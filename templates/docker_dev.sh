#!/usr/bin/env bash
# usage {{{1 ------------------------------------------------------------------
#/ Usage: 
#/        ./dev.sh [OPTIONS] [-B] <builds>
#/    
#/   -h|-?|--help)
#/       show this help and exit
#/
#/   -b|--build)
#/       build an image
#/
#/   -B|--builds)
#/       pass list of directories to build images from. must always be passed
#/       last as it gobbles all trailing arguments
#/
#/   -p|--push)
#/       push the base image
#/
#/   -t|--tag
#/       the tag for the image without the label
#/
#/   -l|--label)
#/       specify label for image
#/
#/   -u|--up)
#/       spin up the docker stack
#/
#/   -P|--pull)
#/       get the latest base image
#/
#/   -i|--interactive)
#/       enter specified container interactively
#/
# 1}}} ------------------------------------------------------------------------
# environment {{{1 ------------------------------------------------------------
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE="$( basename "$DIR")"
TAG="" # Fill with devault path/docker or your.repo.xyz:<port>/<name of image>
LABEL="latest" # Fill with the default
BUILD=0
PUSH=0
UP=0
INTERACTIVE=0
DE=0
RETRIEVE=0
BUILDS=("")
# 1}}} ------------------------------------------------------------------------
# functions {{{1 --------------------------------------------------------------
banner() { # {{{2 -------------------------------------------------------------
  echo -e "\\e[35m"
  echo -e "$(cat << EOF
       _            _             
    __| | ___   ___| | _____ _ __ 
   / _\` |/ _ \ / __| |/ / _ \ '__|
  | (_| | (_) | (__|   <  __/ |   \\e[34mBuildTools\\e[35m
   \__,_|\___/ \___|_|\_\___|_|     \\e[32mBy: \\e[38mJoshua N. Grant\\e[36m
                                        <jngrant9@gmail.com> 
                                
EOF
)"
  echo -e "\\e[39m"
                              
} # 2}}} ----------------------------------------------------------------------
die() { # {{{2 ----------------------------------------------------------------
  echo -e "\\e[31mFAILURE:\\e[39m $1"
  exit 1
} # 2}}} ----------------------------------------------------------------------
info() { # {{{2
  echo -e "\\e[36mINFO:\\e[39m $1"
} # 2}}}
warn() { # {{{2 ---------------------------------------------------------------
  echo -e "\\e[33mWARNING:\\e[39m $1"
} # 2}}} ----------------------------------------------------------------------
show_help() { # {{{2 ----------------------------------------------------------
  grep '^#/' "${BASH_SOURCE[0]}" | cut -c4- || \
    die "Failed to display usage information"
} # 2}}} ----------------------------------------------------------------------
check_volume() { # {{{2 -------------------------------------------------------
  VOLUMES=$(docker volume ls --format "{{.Name}}")
  if echo "$VOLUMES" | grep -q "$1"; then
    info "$1 found"
  else
    warn "creating $1"
    docker volume create --name="$1"
  fi
} # 2}}} ----------------------------------------------------------------------
check_volumes() {
  info 'add the volumes you need to check here'
}
check_network() {
  NETWORKS=$(docker network ls --format "{{.Name}}")
  if echo "$NETWORKS" | grep -q "$1"; then
    info "Network found"
  else
    warn "Creating network"
    docker network create $1
  fi
}
# 1}}} ------------------------------------------------------------------------
# arguments {{{1 --------------------------------------------------------------
while :; do
  case $1 in # check arguments {{{2 -------------------------------------------
    -b|--build-base) # {{{3
      BUILD=1
      shift
      ;; # 3}}}
    -B|--builds) # {{{3
      shift
      BUILDS_LENGTH="$#"
      BUILDS=("$@")
      shift "$BUILDS_LENGTH"
      ;; # 3}}}
    -p|--push) # {{{3
      PUSH=1
      shift
      ;; # 3}}}
    -i|--interactive) # {{{3
      UP=1
      INTERACTIVE=1
      DE="$2"
      shift
      ;; # 3}}}
    -t|--tag) # {{{3
      TAG=$2
      shift 2
      ;; # 3}}}
    -l|--label) # {{{3
      LABEL=$2
      shift 2
      ;; # 3}}}
    -u|--up) # {{{3
      UP=1
      shift
      ;; # 3}}}
    -P|--pull) # {{{3
      RETRIEVE=1
      shift
      ;; # 3}}}
    -h|-\?|--help) # help {{{3 ------------------------------------------------
      banner
      show_help
      exit
      ;; # 3}}} ---------------------------------------------------------------
    -?*) # unknown argument {{{3 ----------------------------------------------
      warn "Unknown option (ignored): $1"
      shift
      ;; # 3}}} ---------------------------------------------------------------
    *) # default {{{3 ---------------------------------------------------------
      break # 3}}} ------------------------------------------------------------
  esac # 2}}} -----------------------------------------------------------------
done
# 1}}} ------------------------------------------------------------------------
# logic {{{1 ------------------------------------------------------------------
banner
IMAGE_TAG="$TAG:$LABEL"
if [ "$RETRIEVE" -eq "1" ]; then
  info "Pulling latest image $IMAGE_TAG"
  docker pull "$IMAGE_TAG"
fi
if [ "$BUILD" -eq "1" ]; then
  info "Building image $IMAGE_TAG"
  docker build -t "$IMAGE_TAG" -f base/Dockerfile base/
fi
if [ "$PUSH" -eq "1" ]; then
  info "Pushing image $IMAGE_TAG"
  docker push "$IMAGE_TAG"
fi
if [ "$UP" -eq "1" ]; then
  info "Spinning up stack"
  docker-compose up -d --build "${BUILDS[@]}"
fi
if [ "$INTERACTIVE" -eq "1" ]; then
  info "Dropping into shell of $DE"
  docker exec -it "${BASE}_${DE}_1" bash
fi
# 1}}} ------------------------------------------------------------------------
