import os
import sys
import time
import xml.etree.ElementTree as ET
from colorama import init, Fore, Back, Style

foundedCodes = []
outputContainer = []
blockCounter = 0
previousCode = ""
fileCreated = False
errors = False

modulesObject = {"7B2":"HUD", "7D0":"APIM", "7E0":"PCM", "706":"IPMA", "716":"GWM", "720":"IPC", "724":"SCCM", "725":"WACM", "726":"BCM-GEM", "727":"ACM", "730":"PSCM", "733":"HVAC", "734":"HCM", "736":"PAM", "737":"RCM", "740":"DDM", "741":"PDM", "754":"TCU", "760":"ABS", "764":"CCM", "7C4":"SODL", "7C6":"SODR", "783":"DSP", "6F0":"BCMC", "775":"LTM", "7B1":"IPMB", "7E6":"FICM", "746":"DCDC", "7C7":"ACCM", "7E4":"BECM", "791":"791", "703":"703", "732":"732", "750":"750"}

fwObject = { 'F124': 'Calibration (CAN, F124)', 'F120': 'Strategy (CAN,F120)', 'F12C': 'F12C', 'F12B': 'F12B', 'F12A': 'F12A', 'F123': 'Strategy (CAN,F123)', 'F121': 'Strategy (CAN F121)', 'F110': 'F110', 'F111': 'Hardware Number', 'F113': 'Calibration Level', 'F188': 'Strategy(CAN, F188)', 'F10A': 'ECU Configuration/Sound Profiles (CAN, F10A)', 'F16B': 'ECU Configuration/Illumination Strategy (CAN, F16B)', 'F18C': 'F18C' }

file_path = sys.argv[1:]


while True:
    user_input = input(f"Start conversion? {Fore.LIGHTGREEN_EX}Y{Style.RESET_ALL} / {Fore.RED}N{Style.RESET_ALL} >> ")
    if user_input == "y" or user_input == "Y":
        tree = ET.parse(file_path[0])
        root = tree.getroot()
        bce_module = root.find(".//BCE_MODULE")
        dataTags = bce_module.findall(".//DATA")
        nodesArr = root.findall(".//NODEID")
        for el in nodesArr:
            foundedCodes.append(el.text.strip())
        carDir = root.find(".//VIN").text

        # create main folder with car code
        try:
            os.mkdir(carDir)
            print("Main folder created..")
        except:
            print(f"{Fore.RED}Something bad is happening.. {Style.RESET_ALL}Cannot create folder. Try running the program with admin privileges.")
        
        # create sub folders with modules names
        for el in foundedCodes:
            if el in modulesObject:
                try:
                    os.mkdir(os.path.join(carDir, modulesObject.get(el)))
                    print(f"Folder of module {modulesObject.get(el)} created.. ✅")
                except:
                    print(f"{Fore.RED}Something bad is happening.. {Style.RESET_ALL}Cannot create folder. Try running the program with admin privileges.")
            else:
                try:
                    os.mkdir(os.path.join(carDir, el))
                    print(f"Folder of module {el} created.. ✅")
                except:
                    print(f"{Fore.RED}Something bad is happening.. {Style.RESET_ALL}Cannot create folder. Try running the program with admin privileges.")
        
        # cycle all data tags
        for data in dataTags:
            label = data.get('LABEL')
            completeStr = ""
            
            codePart = label[:3]
            blockPart = label[-5:-3]
            linePart = label[-2:]

            # check if actual module code is the same, else create new block and switch to next folder module
            if codePart == previousCode:
                pass
            else:
                outputContainer.clear()
                previousCode = codePart
                fileCreated = True
                blockCounter = 0
            
            # check if block number is the same, else append the new Block string
            if int(blockPart) == blockCounter:
                pass
            else:
                blockCounter += 1
                outputContainer.append(f";Block {str(blockCounter)}")
            
            # check and convert block/line number
            if int(blockPart) <= 15:
                completeStr += f"{codePart}G{str(hex(int(blockPart)))[-1:].upper()}"
            elif int(blockPart) > 15 and int(blockPart) <= 31:
                completeStr += f"{codePart}H{str(hex(int(blockPart)))[-1:].upper()}"
            elif int(blockPart) > 31:
                completeStr += f"{codePart}I{str(hex(int(blockPart) - 1))[-1:].upper()}" # -1 fix for hex 0x20

            if int(linePart) <= 15:
                completeStr += f"G{str(hex(int(linePart)))[-1:].upper()}"
            elif int(linePart) > 15 and int(linePart) <= 31:
                completeStr += f"H{str(hex(int(linePart)))[-1:].upper()}"
            elif int(linePart) > 31:
                completeStr += f"I{str(hex(int(linePart) - 1))[-1:].upper()}" # -1 fix for hex 0x20
            
            currentCodesArr = data.findall(".//CODE")

            # cycle code tag content
            for el in currentCodesArr:
                if el.text != None:
                    completeStr += f"{el.text}"

            # finally build the complete string with module codes
            outputContainer.append(completeStr)

            # create abt and FW details on the actual module folder
            # manage exceptions with missing modules references
            # bypass exception with missing modules references by trying to use only the code instead of reference from object
            try:
                f = open(os.path.join(carDir, modulesObject.get(previousCode), f"{carDir}-{modulesObject.get(previousCode)}.abt"), "w")
                for string in outputContainer:
                    f.write(string + '\n')
                f.close()
            except:
                try:
                    f = open(os.path.join(carDir, previousCode, f"{carDir}-{previousCode}.abt"), "w")
                    for string in outputContainer:
                        f.write(string + '\n')
                    f.close()
                except:
                    print(f"{Fore.RED}\nSomething gone wrong writing the ABT file.. {Style.RESET_ALL}Info:\nSuspicious code > {previousCode} < \nErrore -- {modulesObject.get(previousCode)} --\n")
                    errors = True
            
            try:
                fw = open(os.path.join(carDir, modulesObject.get(previousCode), f"{carDir}-{modulesObject.get(previousCode)}-Firmware.txt"), "w")
                for el in nodesArr:
                    if el.text.strip() != previousCode:
                        pass
                    else:
                        for code in el:
                            fw.write(fwObject.get(code.tag) + '\n' + code.text + '\n\n') if code.tag in fwObject else fw.write(code.tag + '\n' + code.text + '\n\n')
                                
            except:
                try:
                    fw = open(os.path.join(carDir, modulesObject.get(previousCode), f"{carDir}-{previousCode}-Firmware.txt"), "w")
                    for el in nodesArr:
                        if el.text.strip() != previousCode:
                            pass
                        else:
                            for code in el:
                                fw.write(fwObject.get(code.tag) + '\n' + code.text + '\n\n') if code.tag in fwObject else fw.write(code.tag + '\n' + code.text + '\n\n')
                except:
                    print(f"{Fore.LIGHTYELLOW_EX}\nModule {previousCode} not in the modulesObject. Consider adding it manually into the main.py {Style.RESET_ALL}")
                    try:
                        fw = open(os.path.join(carDir, previousCode, f"{carDir}-{previousCode}-Firmware.txt"), "w")
                        for el in nodesArr:
                            if el.text.strip() != previousCode:
                                pass
                            else:
                                fw.write(fwObject.get(code.tag) + '\n' + code.text + '\n\n') if code.tag in fwObject else fw.write(code.tag + '\n' + code.text + '\n\n')
                    except:
                        print(f"{Fore.RED}\nSomething gone wrong writing the txt file with the Firmware infos.. {Style.RESET_ALL}Info:\nSuspicious code > {previousCode} <")
                        errors = True
            
            if fileCreated:
                print(f"File of module {modulesObject.get(previousCode)} created and written.. ✅") if previousCode in modulesObject else print(f"File of module {previousCode} created and written.. ✅")
                fileCreated = False

        #delete empty folders 
        for dirpath, dirnames, files in os.walk(carDir):
            if not files:
                if dirpath != carDir:
                    try:
                        os.rmdir(dirpath)
                    except:
                        print(f"{Style.BRIGHT}{Fore.LIGHTYELLOW_EX}Error{Style.RESET_ALL} removing empty folder > {dirpath} <")

        print(f"Folders cleanup completed.. ✅")

        if errors:
            print(f"\n{Style.BRIGHT}{Fore.RED}There are problems.. {Style.RESET_ALL}Check if file AB has any module not included into the modulesObject of the main.py")
        else:
            print(Fore.GREEN + "\nI've done. Looks like everything is fine!")
            time.sleep(1)
            print(f"{Style.BRIGHT}{Fore.CYAN}LizZo {Style.RESET_ALL}is so good :)")
            time.sleep(2)
        
        final_q = input("\nPress Enter to close the program. ")
        if final_q != None:
            print(Style.RESET_ALL + "Closing this awesome program..")
            time.sleep(2)

        break
    elif user_input == "N" or user_input == "n":
        break
    else:
        print("WTF Bruh? \n")
