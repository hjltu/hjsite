#!/bin/bash

#json file generator for homekit2mqtt

if [ -z $3 ]; then
    echo "ERR no accessory input"
    exit 1
fi

ACCESSORY=""
FILE="$HOME/hjhome.json"
#FILE="$HOME/test-hjhome.json"
touch $FILE

########## accessories ###########################

lamp() {
LAMP='
	"Light-'$1'": {
		"service": "Lightbulb",
		"name":    "'$2'",
		"topic": {
			"setOn":    "/homekit/'$1'",
			"statusOn": "/homekit/'$1'-stat"
		},
		"payload": {
			"onTrue":  1,
			"onFalse": 0
		},
		"manufacturer": "hjltu",
		"model": "Lightbulb"
	},
'
ACCESSORY="$ACCESSORY$LAMP"
}

outlet() {
OUTLET='
	"Outlet-'$1'": {
		"service": "Outlet",
		"name":    "'$2'",
		"topic": {
			"setOn":             "/homekit/'$1'",
			"statusOutletInUse": "/homekit/'$1'-stat"
		},
		"payload": {
			"onTrue":  1,
			"onFalse": 0
		},
		"manufacturer": "hjltu",
		"model": "Outlet"
	},
'
ACCESSORY="$ACCESSORY$OUTLET"
}

dimm_lamp() {
DIMM_LAMP='
	"Light-dimm-'$1'": {
		"service":  "Lightbulb",
		"name":     "'$2'",
		"topic": {
			"setOn":            "/homekit/'$1'",
			"setBrightness":    "/homekit/'$1'-dimm",
			"statusOn":         "/homekit/'$1'-stat",
			"statusBrightness": "/homekit/'$1'-dimm-stat"
		},
		"payload": {
			"onTrue": 1,
			"onFalse": 0,
			"brightnessFactor": 2.54
		},
		"manufacturer": "hjltu",
		"model": "Lightbulb Dimmable"
	},
'
ACCESSORY="$ACCESSORY$DIMM_LAMP"
}

rgb_lamp() {
RGB_LAMP='
	"Light-rgb-'$1'": {
		"service":  "Lightbulb",
		"name":     "'$2'",
		"topic": {
			"setOn":            "/homekit/'$1'",
			"setRGB":            "/homekit/'$1'-RGB",
			"setBrightness":    "/homekit/'$1'-br",
			"setHue":           "/homekit/'$1'-hue",
			"setSaturation":    "/homekit/'$1'-sat",
			"statusOn":         "/homekit/'$1'-stat",
			"statusRGB":         "/homekit/'$1'-RGB-stat",
			"statusBrightness": "/homekit/'$1'-br-stat",
			"statusHue":        "/homekit/'$1'-hue-stat",
			"statusSaturation": "/homekit/'$1'-sat-stat"
		},
		"payload": {
			"onTrue":  1,
			"onFalse": 0,
			"brightnessFactor": 2.54,
			"hueFactor": 1,
			"saturationFactor": 2.54
		},
	"manufacturer": "hjltu",
	"model": "Lightbulb Color"
	},
'
ACCESSORY="$ACCESSORY$RGB_LAMP"
}

fan() {
FAN='
	"Fan-'$1'": {
		"service": "Fan",
		"name": "'$2'",
		"topic": {
			"setOn":    "/homekit/'$1'",
			"statusOn": "/homekit/'$1'-stat"
		},
		"payload": {
			"onTrue":  1,
			"onFalse": 0
		},
		"manufacturer": "hjltu",
		"model": "Fan"
	},
'
ACCESSORY="$ACCESSORY$FAN"
}

blinds() {
BLINDS='
	"WindowCowering-'$1'": {
		"service":  "WindowCovering",
		"name": "'$2'",
		"topic": {
			"setTargetPosition":     "/homekit/'$1'",
			"statusTargetPosition":  "/homekit/'$1'-stat",
			"statusCurrentPosition": "/homekit/'$1'-stat"
		},
		"payload": {
			"targetPositionFactor":  2.54,
			"currentPositionFactor": 2.54
		},
		"manufacturer": "hjltu",
		"model": "WindowCovering"
	},
'
ACCESSORY="$ACCESSORY$BLINDS"
}

temp() {
TEMP='
	"TemperatureSensor-'$1'": {
		"service": "TemperatureSensor",
		"name": "'$2'",
		"topic": {
			"statusTemperature": "/homekit/'$1'-curr"
		},
		"manufacturer": "hjltu",
		"model": "TemperatureSensor"
	},
'
ACCESSORY="$ACCESSORY$TEMP"
}

hum() {
HUM='
	"HumiditySensor-'$1'": {
		"service": "HumiditySensor",
		"name": "'$2'",
		"topic": {
			"statusHumidity": "/homekit/'$1'-curr"
		},
		"manufacturer": "hjltu",
		"model": "HumiditySensor"
	},
'
ACCESSORY="$ACCESSORY$HUM"
}

term() {
TERM='
	"Thermostat-'$1'": {
		"service": "Thermostat",
		"name": "'$2'",
		"topic": {
			"setTargetTemperature":             "/homekit/'$1'-target",
			"statusCurrentTemperature":         "/homekit/'$1'-curr",
			"statusTargetTemperature":          "/homekit/'$1'-target-stat",
			"setTargetHeatingCoolingState":     "/homekit/'$1'-mode",
			"statusTargetHeatingCoolingState": "/homekit/'$1'-mode-stat",
			"statusCurrentHeatingCoolingState": "/homekit/'$1'-use-stat"
		},
		"config": {
			"TemperatureDisplayUnits": 0
		},
		"manufacturer": "hjltu",
		"model": "Thermostat"
	},
'
ACCESSORY="$ACCESSORY$TERM"
}

switch() {
SWITCH='
	"Switch-'$1'": {
		"service": "Switch",
		"name": "'$2'",
		"topic": {
			"setOn":    "/homekit/'$1'",
			"statusOn": "/homekit/'$1'-stat"
		},
		"payload": {
			"onTrue":  1,
			"onFalse": 0
		},
		"manufacturer": "hjltu",
		"model": "Switch"
	},
'
ACCESSORY="$ACCESSORY$SWITCH"
}

leak() {
LEAK='
	"LeakSensor-'$1'": {
		"service": "LeakSensor",
		"name": "'$2'",
		"topic": {
			"statusLeakDetected": "/homekit/'$1'-curr"
		},
		"payload": {
			"onLeakDetected": 1
		},
		"manufacturer": "hjltu",
		"model": "LeakSensor"
	},
'
ACCESSORY="$ACCESSORY$LEAK"
}

motion() {
MOTION='
  "MotionSensor-'$1'": {
    "service": "MotionSensor",
    "name": "'$2'",
    "topic": {
      "statusMotionDetected": "/homekit/'$1'-curr"
    },
    "payload": {
      "onMotionDetected": 1
    },
    "manufacturer": "hjltu",
    "model": "MotionSensor"
  },
'
ACCESSORY="$ACCESSORY$MOTION"
}

############### homekit2mqtt mac ##################

mac() {
    MAC=$2
    #if [[ "$MAC" =~ "[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]" ]]; then
    if [[ "$MAC" =~ ^[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]$ ]]; then
        sudo sed -i "s/AA:BB:[0-Z][0-Z]:[0-Z][0-Z]:[0-Z][0-Z]:[0-Z][0-Z]/AA:BB:$MAC/" /etc/systemd/system/hjhome.service
        echo "Homekit MAC changed to: AA:BB:$MAC"
    else
        echo "ERR: Wrong homekit MAC: AA:BB:$MAC"
    fi
}

###################################################

#create accessories
#lamp test лампа

ARGS=`expr $# / 3`
echo "args = $ARGS"
for (( i=0; i<$ARGS; i++ ))
do
    echo "$i create: $1 $2 $3"
    $1 $2 $3
    shift 3
done

#################################################

echo "{$ACCESSORY}" > $FILE

LINE=`cat $FILE | wc -l`
if [ $LINE -gt 10 ]
then
#	echo " remove (,) after last accessory"
	let LINE=$LINE-1
#	echo "$LINE"
	sed -i "${LINE}s/,//" $FILE
else
	echo "ERR no accessories in $FILE"
    exit 1
fi
echo "OK"
exit 0
#cat $FILE



























