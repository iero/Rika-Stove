-- Greg FABRE - 2017

-- Thermostat regulation using domoticz setpoint system
-- Place this file in domoticz/scripts/lua directory
-- Update local variable according to Thermostat name and rika_command according to script location

local rika_thermostat = 'Rika Thermostat'
local rika_command = '/usr/bin/python /home/pi/Rika-Stove/rika.py /home/pi/Rika-Stove/settings.xml set '

commandArray = {}

if (devicechanged[rika_thermostat]) then
        print('[Thermostat Rika] changed to '..otherdevices_svalues[rika_thermostat])
        cmd_success=os.execute(rika_command..otherdevices_svalues[rika_thermostat])
        print(cmd_success)
        if not cmd_success then
                print("Failed updating rika stove")
        end
end

return commandArray
