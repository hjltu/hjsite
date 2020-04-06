#!/bin/bash

#json file generator for homekit2mqtt

if [ -z $3 ]; then
    echo "ERR no accessory input"
    exit 1
fi

ACCESSORY=$1
FILE="$HOME/hjhome.json"
#FILE="$HOME/test-hjhome.json"
touch $FILE
echo "{" > $FILE

########## accessories ###########################

lamp() {
LAMP="
\t	\"Light-$1\": {\n
\t	\t	\"service\": \"Lightbulb\",\n
\t	\t	\"name\":    \"$2\",\n
\t	\t	\"topic\": {\n
\t	\t	\t	\"setOn\":    \"/homekit/$1\",\n
\t	\t	\t	\"statusOn\": \"/homekit/$1-stat\"\n
\t	\t	},\n
\t	\t	\"payload\": {\n
\t	\t	\t	\"onTrue\":  1,\n
\t	\t	\t	\"onFalse\": 0\n
\t	\t	},\n
\t	\t	\"manufacturer\": \"Generic\",\n
\t	\t	\"model\": \"Lightbulb\"\n
\t	},\n"
echo -e $LAMP >> $FILE
}

outlet() {
OUTLET="
\t	\"Outlet-$1\": {\n
\t	\t	\"service\": \"Outlet\",\n
\t	\t	\"name\":    \"$2\",\n
\t	\t	\"topic\": {\n
\t	\t	\t	\"setOn\":             \"/homekit/$1\",\n
\t	\t	\t	\"statusOutletInUse\": \"/homekit/$1-stat\"\n
\t	\t	},\n
\t	\t	\"payload\": {\n
\t	\t	\t	\"onTrue\":  1,\n
\t	\t	\t	\"onFalse\": 0\n
\t	\t	},\n
\t	\t	\"manufacturer\": \"Generic\",\n
\t	\t	\"model\": \"Outlet\"\n
\t	},\n"
echo -e $OUTLET >> $FILE
}

dimm_lamp() {
DIMM_LAMP="
\t	\"Light-dimm-$1\": {\n
\t	\t	\"service\":  \"Lightbulb\",\n
\t	\t	\"name\":     \"$2\",\n
\t	\t	\"topic\": {\n
\t	\t	\t	\"setOn\":            \"/homekit/$1\",\n
\t	\t	\t	\"setBrightness\":    \"/homekit/$1-dimm\",\n
\t	\t	\t	\"statusOn\":         \"/homekit/$1-stat\",\n
\t	\t	\t	\"statusBrightness\": \"/homekit/$1-dimm-stat\"\n
\t		},\n
\t		\"payload\": {\n
\t	\t	\t	\"onTrue\": 1,\n
\t	\t	\t	\"onFalse\": 0,\n
\t	\t	\t	\"brightnessFactor\": 2.54\n
\t	\t	},\n
\t	\t	\"manufacturer\": \"Generic\",\n
\t	\t	\"model\": \"Lightbulb Dimmable\"\n
\t	},\n"
echo -e $DIMM_LAMP >> $FILE
}

rgb_lamp() {
RGB_LAMP="
\t	\"Light-rgb-$1\": {\n
\t	\t	\"service\":  \"Lightbulb\",\n
\t	\t	\"name\":     \"$2\",\n
\t	\t	\"topic\": {\n
\t	\t	\t	\"setOn\":            \"/homekit/$1\",\n
\t	\t	\t	\"setBrightness\":    \"/homekit/$1-br\",\n
\t	\t	\t	\"setHue\":           \"/homekit/$1-hue\",\n
\t	\t	\t	\"setSaturation\":    \"/homekit/$1-sat\",\n
\t	\t	\t	\"statusOn\":         \"/homekit/$1-stat\",\n
\t	\t	\t	\"statusBrightness\": \"/homekit/$1-br-stat\",\n
\t	\t	\t	\"statusHue\":        \"/homekit/$1-hue-stat\",\n
\t	\t	\t	\"statusSaturation\": \"/homekit/$1-sat-stat\"\n
\t	\t	},\n
\t	\t	\"payload\": {\n
\t	\t	\t	\"onTrue\":  1,\n
\t	\t	\t	\"onFalse\": 0,\n
\t	\t	\t	\"brightnessFactor\": 2.54,\n
\t	\t	\t	\"hueFactor\": 1,\n
\t	\t	\t	\"saturationFactor\": 2.54\n
\t	\t	},\n
\t	\"manufacturer\": \"Generic\",\n
\t	\"model\": \"Lightbulb Color\"\n
\t	},\n"
echo -e $RGB_LAMP >> $FILE
}

fan() {
FAN="
\t	\"Fan-$1\": {\n
\t	\t	\"service\": \"Fan\",\n
\t	\t	\"name\": \"$2\",\n
\t	\t	\"topic\": {\n
\t	\t	\t	\"setOn\":    \"/homekit/$1\",\n
\t	\t	\t	\"statusOn\": \"/homekit/$1-stat\"\n
\t	\t	},\n
\t	\t	\"payload\": {\n
\t	\t	\t	\"onTrue\":  1,\n
\t	\t	\t	\"onFalse\": 0\n
\t	\t	},\n
\t	\t	\"manufacturer\": \"Generic\",\n
\t	\t	\"model\": \"Fan\"\n
\t	},\n"
echo -e $FAN >> $FILE
}

blinds() {
BLINDS="
\t	\"WindowCowering-$1\": {\n
\t	\t	\"service\":  \"WindowCovering\",\n
\t	\t	\"name\": \"$2\",\n
\t	\t	\"topic\": {\n
\t	\t	\t	\"setTargetPosition\":     \"/homekit/$1\",\n
\t	\t	\t	\"statusTargetPosition\":  \"/homekit/$1-stat\",\n
\t	\t	\t	\"statusCurrentPosition\": \"/homekit/$1-stat\"\n
\t	\t	},\n
\t	\t	\"payload\": {\n
\t	\t	\t	\"targetPositionFactor\":  2.54,\n
\t	\t	\t	\"currentPositionFactor\": 2.54\n
\t	\t	},\n
\t	\t	\"manufacturer\": \"Generic\",\n
\t	\t	\"model\": \"WindowCovering\"\n
\t	},\n"
echo -e $BLINDS >> $FILE
}

temp() {
TEMP="
\t	\"TemperatureSensor-$1\": {\n
\t	\t	\"service\": \"TemperatureSensor\",\n
\t	\t	\"name\": \"$2\",\n
\t	\t	\"topic\": {\n
\t	\t	\t	\"statusTemperature\": \"/homekit/$1\"\n
\t	\t	},\n
\t	\t	\"manufacturer\": \"Generic\",\n
\t	\t	\"model\": \"TemperatureSensor\"\n
\t	},\n"
echo -e $TEMP >> $FILE
}

term() {
TERM="
\t	\"Thermostat-$1\": {\n
\t	\t	\"service\": \"Thermostat\",\n
\t	\t	\"name\": \"$2\",\n
\t	\t	\"topic\": {\n
\t	\t	\t	\"setTargetTemperature\":             \"/homekit/$1-target\",\n
\t	\t	\t	\"statusCurrentTemperature\":         \"/homekit/$1-curr\",\n
\t	\t	\t	\"statusTargetTemperature\":          \"/homekit/$1-target-stat\",\n
\t	\t	\t	\"setTargetHeatingCoolingState\":     \"/homekit/$1-mode\",\n
\t	\t	\t	\"statusCurrentHeatingCoolingState\": \"/homekit/$1-mode-stat\"\n
\t	\t	},\n
\t	\t	\"config\": {\n
\t	\t	\t	\"TemperatureDisplayUnits\": 0\n
\t	\t	},\n
\t	\t	\"manufacturer\": \"Generic\",\n
\t	\t	\"model\": \"Thermostat\"\n
\t	},\n"
echo -e $TERM >> $FILE
}

switch() {
SWITCH="
\t	\"Switch-$1\": {\n
\t	\t	\"service\": \"Switch\",\n
\t	\t	\"name\": \"$2\",\n
\t	\t	\"topic\": {\n
\t	\t	\t	\"setOn\":    \"/homekit/$1\",\n
\t	\t	\t	\"statusOn\": \"/homekit/$1-stat\"\n
\t	\t	},\n
\t	\t	\"payload\": {\n
\t	\t	\t	\"onTrue\":  1,\n
\t	\t	\t	\"onFalse\": 0\n
\t	\t	},\n
\t	\t	\"manufacturer\": \"Generic\",\n
\t	\t	\"model\": \"Switch\"\n
\t	},\n"
echo -e $SWITCH >> $FILE
}

leak() {
LEAK="
\t	\"LeakSensor-$1\": {\n
\t	\t	\"service\": \"LeakSensor\",\n
\t	\t	\"name\": \"$2\",\n
\t	\t	\"topic\": {\n
\t	\t	\t	\"statusLeakDetected\": \"/homekit/$1-stat\"\n
\t	\t	},\n
\t	\t	\"payload\": {\n
\t	\t	\t	\"onLeakDetected\": true\n
\t	\t	},\n
\t	\t	\"manufacturer\": \"Generic\",\n
\t	\t	\"model\": \"LeakSensor\"\n
\t	},\n"
echo -e $LEAK >> $FILE
}

motion() {
MOTION="
\t  \"LeakSensor-$1\": {\n
\t  \t  \"service\": \"MotionSensor\",\n
\t  \t  \"name\": \"$2\",\n
\t  \t  \"topic\": {\n
\t  \t  \t  \"statusMotionDetected\": \"/homekit/$1-stat\"\n
\t  \t  },\n
\t  \t  \"payload\": {\n
\t  \t  \t  \"onMotionDetected\": true\n
\t  \t  },\n
\t  \t  \"manufacturer\": \"Generic\",\n
\t  \t  \"model\": \"MotionSensor\"\n
\t  },\n"
echo -e $MOTION >> $FILE
}

###################################################

#create accessories
#lamp test лампа

for (( i=0; i<=$#; i++ ))
do
    echo "create: $1 $2 $3"
    $1 $2 $3
    shift 3
    sleep 0.5
done

#################################################

echo "}" >> $FILE

LINE=`cat $FILE | wc -l`
if [ $LINE -gt 10 ]
then
#	echo " remove (,) after last accessory"
	let LINE=$LINE-2
#	echo "$LINE"
	sed -i "${LINE}s/,//" $FILE
else
	echo "ERR no accessories in $FILE"
    exit 1
fi
echo "OK"
exit 0
#cat $FILE



























