#!/bin/sh
export DAC_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/
echo "DAC_ROOT = $DAC_ROOT"

. $DAC_ROOT/dac.config

function kill_container()
{
  $DAC_ROOT/scripts/kill.sh
  exit
}

export DAC_APP=$1
if [ -z $DAC_APP ]; then
  echo Please provide appname!
  exit
fi

if [ -z $DAC_PLATFORM ]; then
  export DAC_PLATFORM=$2
fi

if [ -z $DAC_PLATFORM ]; then
  echo No DAC platform set. Using default!
  export DAC_PLATFORM=7218refapp
fi
echo "DAC_APP = $DAC_APP"
echo "DAC_PLATFORM = $DAC_PLATFORM"

export DAC_APP_ROOT=${DAC_ROOT}apps/$DAC_APP

if [ ! -f "$DAC_APP_ROOT/config.json.template" ]; then
  mkdir -p $DAC_APP_ROOT
  cd $DAC_APP_ROOT
  ${DAC_ROOT}scripts/prepare.sh && ${DAC_ROOT}scripts/download.sh $DAC_APP && ${DAC_ROOT}scripts/unpack.sh
else
  cd $DAC_APP_ROOT
fi
${DAC_ROOT}scripts/run.sh $DAC_PLATFORM &

trap kill_container SIGINT SIGTERM
while true
do
    sleep 1
done
