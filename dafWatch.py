from decimal import Decimal
import time
from watchdog.observers.polling import PollingObserver
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import shutil
import re
import smtplib, ssl
import datetime
import mflib
import string
import json
from logzero import logger, logfile
import pprint
import yagmail
import cuid
import requests
import random
from utilities import * 
import unicodedata
from countrycodes import *
import copy
import sentry_sdk
import shortuuid
import pandas as pd
import csv
from xml.sax.saxutils import escape
sentry_sdk.init(
    "https://571df95b8f2a4177a34f81ef9d0605db@o488161.ingest.sentry.io/5573871",
    traces_sample_rate=1.0
)

import csv


#####to multifreight live link for config.json
# "tomultifreight": "/mnt/entry_and_job"
#"/sftpusers/chroot/electrolux" ##for in and watch
##for test "tomultifreight": "/home/jon/paccar-edi-in/processing/tomultifreight"


with open('config.json') as config_file:
    config_data = json.load(config_file)

logfile(config_data["log"], maxBytes=1e6, backupCount=3)
# Log messages
logger.info("Program started")

WatchDirectory = config_data["watch"]
in_folder = config_data["in_folder"]
out_folder = config_data["out_folder"]
error_folder = config_data["error_folder"]
temp = config_data["temp"]
tomultifreight = config_data["tomultifreight"]
hsFailPath = config_data['hsFailPath']

port = 25
acemail = yagmail.SMTP(user = 'ace@forwarding.digital', smtp_skip_login=True, password = '3j!634ru', host='192.168.70.106', port=port, smtp_starttls=False, smtp_ssl=False)  
jhmail = yagmail.SMTP(user='jon.heavyside@trilogyfreight.com', password='j6w8w534j6w8w534',
                      host='smtp.office365.com', port=587, smtp_starttls=True, smtp_ssl=False)


def getHsDetails(hS):
    try:
        urltorequest = f"https://api.forwarding.digital/hscommodities"
        jsonBody = {
            "hsCode": hS
        }
        #print(jsonBody)
        response = requests.post(urltorequest, json=jsonBody, headers={'appID': 'HhzI0HoFeexFX4s7MxIAz6zBChvrBbTSVAu7Zwn63'})
        rj = response.json()
        #print(rj)
        if rj['status'] == "Success":
            response = {
                "dutyRate": rj['dutyRate'],
                "vatStandard": rj['vatStandard'],
                "vatZero": rj['vatZero'],
                "vatA": rj['vatA'],
                "valid": True,
                "supplementaryUnits": rj['supplementaryUnits']
            }
        else:
            response = {
                "dutyRate": None,
                "vatStandard": None,
                "vatZero": None,
                "vatA": None,
                "valid": False,
                "supplementaryUnits": False
            }  

        return response

      
    except Exception as e:
        logger.warning(f" {e.__class__.__name__}: {e} - Couldn't get hs -- {hS} Info") 
        logger.exception(e)
        sentry_sdk.capture_exception(e) 
        response = {
                "dutyRate": None,
                "vatStandard": None,
                "vatZero": None,
                "vatA": None,
                "valid": False,
                "supplementaryUnits": False

            } 

    return response

def checkHs(hS):
    try:
        urltorequest = f"https://api.forwarding.digital/hstest"
        lenHs = len(hS)
        if lenHs != 10:
            return False
        jsonBody = {
            "hsCode": hS
        }
        #print(jsonBody)
        response = requests.post(urltorequest, json=jsonBody, headers={'appID': 'HhzI0HoFeexFX4s7MxIAz6zBChvrBbTSVAu7Zwn63'})
        rj = response.json()
        #print(rj)
        statusBack = rj.get('isvalid')
        if statusBack == None or statusBack == False:
            return False    
        else:
            return True

      
    except Exception as e:
        logger.warning(f" {e.__class__.__name__}: {e} - Couldn't verify hs -- {hS} Info") 
        logger.exception(e)
        sentry_sdk.capture_exception(e) 

    return False   


def Ducr(Reference, Direction):
    try:
        now = datetime.datetime.today()
        day = now.strftime("%y")
        Lday = day[-1:]
        r1 = str(random.randint(0,9))
        r2 = str(random.randint(0,9))
        r3 = str(random.randint(0,9))
        CVat = "GB548600440000"
        pattern = re.compile('\W')
        ReferenceStr = re.sub(pattern, '', Reference)
        uniqueref = shortuuid.uuid()
        uniquerefS = uniqueref[0:11]

        if Direction == "Import":
            DucrS = Lday + CVat + "-" + uniquerefS
        elif Direction == "Export":
            DucrS = Lday + CVat + "-" + uniquerefS
        else:
            DucrS = Lday + CVat + "-" + uniquerefS    
    except Exception as e:
        logger.warning(f" {e.__class__.__name__}: {e} - Couldn't Create DUCR")    
        logger.exception(e)
        sentry_sdk.capture_exception(e) 
        DucrS = "22GB548600440000" + shortuuid.uuid()[0:11]   

    return DucrS    



def checkhs8(hs8, cominvref):
    hs8Count = len(hs8)
    if hs8Count == 9:
        hs8 = hs8[0:8]      ##if they supply a 9 digit hs code delete the last character - from jakob strych email 8th Feb confirmaing action
    for x in comtrans:
        hs8List = x['hs8']
        #print(hs8List)
        if hs8List == hs8:
            hs10 = x['hs10']  
            #print(f"found comodditycode - {hs10}")  
            return hs10
    else:
        contentsEmail = f"Please note your reference {cominvref} contains an unmapped commodity code - {hs8}. <br/><br/>Please contact us urgently so we can resolve this to a code and transmit your entry." 
        jhmail.send(to="jheavyside@trilogyfreight.com", subject=f"{cominvref} contains unmapped HS code", contents=genEmail(contentsEmail))
        jhmail.send(to="howden@cargo-overseas.co.uk", subject=f"{cominvref} contains unmapped HS code", contents=genEmail(contentsEmail))
        return False        

class Watcher:
    DIRECTORY_TO_WATCH = WatchDirectory

    def __init__(self):
        self.observer = PollingObserver()   #   Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            file_name = os.path.basename(event.src_path)#grab the filename of the found file
            move_path = out_folder + "/" + file_name
            error_path = error_folder + "/" + file_name
            hsFailFolder = hsFailPath + "/" + file_name
            error_path_failed_hs8 = error_folder + "/" + file_name
            failHs8Test = False
            from_path = in_folder + "/" + file_name
            outFullPath = out_folder + "/p-" + file_name
            FileName = os.path.splitext(file_name)#seperate the filetype for error handling
            FileTypeIn = (FileName[1])
            time.sleep(0.5)#Add a delay in for windows
            if FileTypeIn != ".csv":#kick out anything not an xml
                try:
                    os.replace(from_path, error_path)
                    logger.error(file_name + " is not an .csv")
                except Exception as e:
                        logger.warning(f" {e.__class__.__name__}: {e} - error moving file from edi in to error folder ")    
                        return    
            else:
                #try:
                logger.info(f"attempted to read {file_name}...")
                _fo = open(event.src_path,"r", encoding='unicode_escape')
                try:
                    df = pd.read_csv(event.src_path, encoding='unicode_escape')
                #df = df.applymap(str)
                    mainObject = df.to_dict('records')
                except Exception as e:
                        logger.warning(f" {e.__class__.__name__}: {e} - cread file - encoding issue ")    
                        return
                #pprint.pprint(mainObject)
                _fo.close()
                ##check all items bfore proceeding
                hsCheck = True
                hsInvalidCodes = []
                hsInvalidCodesSet = set()

                logger.info(f"checking hsCodes ...")
                for i in mainObject:
                    hsCode = str(i['Commodity code (10)'])
                    ##check if it needs patching
                    patchHsCodeTest = hs10Translate(hsCode)
                    isGoodHs = checkHs(hsCode)
                    if isGoodHs:
                        if patchHsCodeTest: ##patch the code in the dictionary if we need to
                            i['Commodity code (10)'] = patchHsCodeTest
                    else:
                        hsCheck = False
                        hsInvalidCodes.append(hsCode)
                        hsInvalidCodesSet.add(hsCode)

                if not hsCheck:
                    contentsEmail = f"Please note reference {file_name} contains {len(hsInvalidCodesSet)} invalid hscode/s used on {len(hsInvalidCodes)} items<br/><br/>{hsInvalidCodesSet}<br/><br/>This has been moved to the hs wrong codes list folder" 
                    jhmail.send(to="jheavyside@trilogyfreight.com", subject=f"{file_name} contains invalid hsCodes", contents=genEmail(contentsEmail))
                    jhmail.send(to="howden@cargo-overseas.co.uk", subject=f"{file_name} contains invalid hsCodes", contents=genEmail(contentsEmail))
                    os.replace(from_path, hsFailFolder)
                    logger.info(f"file {file_name} contains {len(hsInvalidCodes)} invalid codes - {hsInvalidCodes}")
                    return 

                ##all codes are good up to here so lets proceed with the entry
                logger.info(f"all hscodes are good so starting the entry")
                FileNameType = os.path.splitext(file_name)
                FileNameName = FileName[0]
                numberOfItems = len(mainObject)
                logger.info(f"*****************")
                logger.info(f"**             **")
                logger.info(f"**  NEW ENTRY  **")
                logger.info(f"**             **")
                logger.info(f"*****************")
                logger.info(f"picked up new file - {file_name}")
                logger.info(f"processing items numbers ... - {file_name}")
                itemsNoTest = numberOfItems < 100
                customerReference = str(mainObject[0]['JobReference'])
                if not itemsNoTest:
                    contentsEmail = f"Please note your reference {customerReference} contains too many items and needs to be split down in order to produce a valid entry. <br/><br/>Please contact us urgently so we can transmit your entry.<br/><br/>This has been moved to the error folder" 
                    jhmail.send(to="jheavyside@trilogyfreight.com", subject=f"{customerReference} contains too many items", contents=genEmail(contentsEmail))
                    jhmail.send(to="howden@cargo-overseas.co.uk", subject=f"{customerReference} contains too many items", contents=genEmail(contentsEmail))
                    os.replace(from_path, error_path)
                logger.info(f"found {numberOfItems} items for reference {customerReference}")
                logger.info(f"processing entry...")
                
                
                callType = "L" #L = Live, T = Test
                Mode = mainObject[0]['Mode of Transport']
                modeTest = Mode.title() == "Road"
                #pprint.pprint(mainObject)

                ##taken out 20/10/21 to process all as advised by gregg
                # if not modeTest:
                #     airFolder = config_data['air_folder']
                #     airPath = airFolder + "/" + file_name
                #     contentsEmail = f"Found an air csv - ref - {customerReference}<br/><br/><br/><br/>This has been moved to the air folder" 
                #     jhmail.send(to="jheavyside@trilogyfreight.com", subject=f"{customerReference} moved to air folder", contents=genEmail(contentsEmail))
                #     jhmail.send(to="howden@cargo-overseas.co.uk", subject=f"{customerReference} moved to air folder", contents=genEmail(contentsEmail))
                #     os.replace(from_path, airPath)
                #     return False

                internalAccount = "DAFT008"
                AddressCode = "DAFT008"     #test account live use modelData['customerID']
                billingRef = mainObject[0]['JobReference']
                customerReference = str(mainObject[0]['JobReference'])
                file_name = str(AddressCode) + '-' + customerReference + " -I"
                portalID = cuid.cuid()
                LoadType = 'DAFBULK' #advised by PC 10/06/21
                PackType = 'PIECES'
                ProductDescription = 'CUSTOMS ENTRY ONLY'  
                internalDeferment = False  
                TransportType = "6"
                if internalDeferment:
                    FirDanPfx = "A"
                    FirDan = "8877913"
                else:    
                    FirDanPfx = 'B'   # it will allways pick this up
                    FirDan = "6172998"
                DecltCity = 'MANCHESTER'    # if on behalf of agent eg toll. then toll woul dbe the declarant
                DecltCntry = 'GB'           # if a shipper then it is always co. need to potentially add a user group:agent and use their address
                DecltName = 'CARGO OVERSEAS'    # for the declarant. we are assuming all ace entries are from shippers not agents and cargo will be the declarant
                DecltPostcode = 'M25 9NJ'
                DecltStreet = 'FLOATS ROAD'
                DecltTid = 'GB548600440000'
                QtyCode = '23'  #net weight set as kg's on the items
                ItemAiStmt = 'LIC99'
                ItemDocCode = 'N934'
                #itemDocStatus = "AE" if euPreferenceDocument != "U112" else "JP"


                PrevDocClass = 'Z'
                PrevDocType = '380'
                if internalAccount:
                    if internalDeferment:
                        MopCodeD = "F"
                    else:
                        MopCodeD = 'F'
                else:    
                    MopCodeD = "F"     # if fas = "D" if importer = "F"
                
                Preference = '100'      ##overridden in the loop if eu preference is set per item level
                Terms = "DAP"   ##hardcoded as per convo with damian
                ValMthdCode = '1'   #Damian says always 1
                DeclnType = "IMD"       #DMC - Allways be IMD
                if Terms == "EXW": 
                    ValAdjtCode = "A"
                elif Terms == "FOB":    
                    ValAdjtCode = "A"
                elif Terms == "CIF":
                    ValAdjtCode = "B"   #gords advised
                elif Terms == "DDP":
                    ValAdjtCode = "D"
                elif Terms == "DAP":
                    ValAdjtCode = "G"    
                else: 
                    ValAdjtCode = "C"    
                    
                Direction = "Import"    ##needed for the mflib generation
                Dept = "SRI"
                RouteCode = "RI"
                PortReceipt = "GB" + mainObject[0]['Port of Arrival']
                ReceiptDesc = "" # need the description in the object
                PortLoading = mainObject[0]['Port of Departure']            # only used for multifreght job generation
                PortLoadingDesc = ""     #
                #UkPort = "GBKGH"
                #PolDescription = Template['PolDescription']        #doesnt seem to be used
                PortofDischarge = "GB" + mainObject[0]['Port of Arrival']
                PortofDischargeDesc = ""
                ConsignorName = mainObject[0]['ConsignorName']
                ConsignorAddress1 = mainObject[0]['ConsignorAddress']
                #ConsignorAddress2 = Template['ConsignorAddress2']
                ConsignorCountryName = mainObject[0]['ConsignorCity']
                ConsignorCounty = mainObject[0]['ConsignorCity'] 
                ConsignorCountry = mainObject[0]['ConsignorCountryCode'] #need to get the 2 digit format
                ConsignorPostcode = str(mainObject[0]['ConsignorPostcode'])
                PortImport = "GB" + mainObject[0]['Port of Arrival']          #eg DOVER. needs to be the long description
                #PortImportCode = "KIL"      #customs code eg DOV
                PortCode = mainObject[0]['Port of Arrival']               #same as above DOV
                DecltRep = "2"              #always 2
                DispCntry = "IT"   #espatch country Needs to be from country 2 letters
                DeclnType = DeclnType      
                LocnCode = "GB" + mainObject[0]['Port of Arrival']    # eg GBDOV needs 
                TrptModeCode = TransportType
                CnsgeCity = mainObject[0]['ConsigneeCity']             #consignee = To address
                CnsgeName = mainObject[0]['ConsigneeName']
                CnsgePostcode = mainObject[0]['ConsigneePostcode']
                CnsgeStreet = mainObject[0]['ConsigneeAddress']
                CnsgeCntry = mainObject[0]['ConsigneeCountryCode']
                CnsgeTid = mainObject[0]['IE-ConsigneeCode']     #= eori
                CnsgrCity = ConsignorCounty
                CnsgrCntry = ConsignorCountry
                CnsgrName = ConsignorName             #consignor = from address
                CnsgrPostCode = ConsignorPostcode
                CnsgrStreet = ConsignorAddress1
                ImporterName = CnsgeName
                ImporterAddress1 = CnsgeStreet
                #ImporterAddress2 = Template['ImporterAddress2']        #dont have this
                ImporterCounty = CnsgeCity
                ImporterCountry = CnsgeCntry
                CountryDespatch = ConsignorCountry
                arrivalDate = datetime.datetime.now()
                IntdArrDtm = arrivalDate.strftime('%Y%m%d%H%M')
                EntType = "SDI"                        #mf default SAD
                Cur = mainObject[0]['CurrencyCode']
                inventory = None
                ukPortCode = mainObject[0]['Port of Arrival']
                ukPortCodes = ["MAN", "LHR", "BHX", "MAN", "FXT", "SOU", "TIL", "LIV", "LON", "GRG", "MNC", "MID", "IMM", "HUL", "FXT", "TIL"]
                InvLinked = ukPortCode in ukPortCodes
                JobPortofReceipt = "GB" + ukPortCode if InvLinked else "GBFXT"
                JobPortofReceiptAir = ukPortCode if InvLinked else "FXT"
                itemsDutyTest = []
                dutyTrue = True  ##I think this should be None or false???   ##used by the duty generation script if there is duty in an item to appen to the itemsDutytest list
                # set the deferred vat status:
                deferredAccounting = True  #needs to be reflective of their choice if api user set to true for them
                # if deferredAccounting == None:
                #     deferredAccounting = True 
                #set eu preference option
                # euPreference = True       ##moved to items array
                # if euPreference == None:
                #     euPreference = True     ##If api user set this option to True as it is a general opt out setting
                bulkPackages = ["VG", "VQ", "VL", "VS", "VY", "VR", "VO"]

                # generic totals
                whatList = mainObject
                #pprint.pprint(x)
                
                NWTotal = str("{:.2f}".format(round((sum([float(z['NetMass']) for z in mainObject])), 2)))
                #ItemsTotal = str(modelData['entry']['header']['totalNumPieces'])
                PiecesTotal = str(sum([int(z['ItemPackageQuantity']) for z in mainObject]))
                Total = str(mainObject[0]['InvoiceAmount'])
                InvNr = str(mainObject[0]['JobReference'])
                TrptId = str(mainObject[0]['Transport ID'])
                # generate Ducr
                DucrS = Ducr(InvNr, Direction)
                PortLoadingAir = PortLoading[2:5]
                PortofDischargeAir = PortofDischarge[2:5]

                multiFreightXML = mflib.MFXml()

                #   job header
                multiFreightXML.isledi.tables.job_hdr.job_route = RouteCode
                multiFreightXML.isledi.tables.job_hdr.receipt = PortReceipt
                multiFreightXML.isledi.tables.job_hdr.receipt_desc = ReceiptDesc if InvLinked else "Felixstowe"
                multiFreightXML.isledi.tables.job_hdr.port_of_loading = PortLoadingAir if Mode == "Air" else PortLoading
                multiFreightXML.isledi.tables.job_hdr.pol_description = PortLoadingDesc
                multiFreightXML.isledi.tables.job_hdr.edi_status = portalID                #not sure this exists yet
                multiFreightXML.isledi.tables.job_hdr.cust_ref = customerReference
                multiFreightXML.isledi.tables.job_hdr.port_of_discharge = JobPortofReceiptAir if Mode == "Air" else JobPortofReceipt
                multiFreightXML.isledi.tables.job_hdr.pod_description = PortofDischargeDesc
                multiFreightXML.isledi.tables.job_hdr.address_code = AddressCode
                #multiFreightXML.isledi.tables.job_hdr.chg_weight = ChgWgt
                multiFreightXML.isledi.tables.job_hdr.consignee_name = CnsgeName
                multiFreightXML.isledi.tables.job_hdr.consignee_town = CnsgeCity
                multiFreightXML.isledi.tables.job_hdr.consignee_ctry = CnsgeCntry
                multiFreightXML.isledi.tables.job_hdr.consignor_name = ConsignorName
                multiFreightXML.isledi.tables.job_hdr.consignor_town = ConsignorCounty
                multiFreightXML.isledi.tables.job_hdr.consignor_ctry = ConsignorCountry
                multiFreightXML.isledi.tables.job_hdr.terms_location = str(arrivalDate)
                multiFreightXML.isledi.tables.job_hdr.entered_wgt = NWTotal
                multiFreightXML.isledi.tables.job_hdr.invoicee = AddressCode
                multiFreightXML.isledi.tables.job_hdr.job_dept = Dept
                multiFreightXML.isledi.tables.job_hdr.kgs_weight = NWTotal
                multiFreightXML.isledi.tables.job_hdr.load_type = LoadType
                multiFreightXML.isledi.tables.job_hdr.package_type = PackType
                multiFreightXML.isledi.tables.job_hdr.pieces = PiecesTotal
                multiFreightXML.isledi.tables.job_hdr.product_desc = ProductDescription
                multiFreightXML.isledi.tables.job_hdr.cust_ref = f"{InvNr} -- {len(mainObject)}"

                # job line - list
                JobLine1 = mflib.JobLine()
                JobLine1.cargo_desc = ProductDescription
                JobLine1.chg_wgt = NWTotal
                JobLine1.consignee_name = CnsgeName
                JobLine1.consignee_town = CnsgeCity
                JobLine1.consignee_ctry = CnsgeCntry
                JobLine1.consignor_name = ConsignorName
                JobLine1.consignor_town = ConsignorCounty
                JobLine1.consignor_ctry = ConsignorCountry
                # JobLine1.cube = ''         Don't have this in the data
                JobLine1.cube_type = 'cbm'
                # JobLine1.entered_cube = ''     Don't have this only weight
                JobLine1.entered_wgt = NWTotal
                JobLine1.kgs_wgt = NWTotal
                JobLine1.line_no = '1'
                JobLine1.package_type = PackType
                JobLine1.pieces = PiecesTotal
                #JobLine1.product_code = PackType   #multifreight specific
                multiFreightXML.isledi.tables.job_line.append(JobLine1)

                #  docadds
                DocAdd1 = mflib.DocAdd()
                DocAdd1.name = CnsgeName
                DocAdd1.town = CnsgeCity
                DocAdd1.country_code = CnsgeCntry
                DocAdd1.address_type = 'CONSEE'
                multiFreightXML.isledi.tables.doc_adds.append(DocAdd1)

                DocAdd2 = mflib.DocAdd()
                DocAdd2.name = ConsignorName
                DocAdd2.town = ConsignorCounty
                DocAdd2.country_code = ConsignorCountry
                DocAdd2.address_type = 'CONSOR'
                multiFreightXML.isledi.tables.doc_adds.append(DocAdd2)

                # start the customs entry
                multiFreightXML.msedi_imports.context.arrived = "false"
                multiFreightXML.msedi_imports.context.send_msg = "false"

                #multiFreightXML.msedi_imports.customs = mflib.Customs()
                multiFreightXML.msedi_imports.customs.customs_ref = 'replace-job-disp'
                multiFreightXML.msedi_imports.customs.mfrt_job_id = 'replace-mfrt-job-id'
                multiFreightXML.msedi_imports.customs.agent_code = 'CARG013'
                multiFreightXML.msedi_imports.customs.consignor_name = ConsignorName
                multiFreightXML.msedi_imports.customs.portcode = PortCode
                multiFreightXML.msedi_imports.customs.decln_ucr = DucrS

                
                multiFreightXML.msedi_imports.customs.consignor_address.append( #this tag is a list
                    ConsignorAddress1)
                #multiFreightXML.msedi_imports.customs.consignor_address.append(    #if you need a second
                #  ConsignorAddress2)
                multiFreightXML.msedi_imports.customs.consignor_county = ConsignorCounty
                multiFreightXML.msedi_imports.customs.consignor_country = ConsignorCountry
                multiFreightXML.msedi_imports.customs.enttype = EntType
                multiFreightXML.msedi_imports.customs.importer_name = ImporterName

                multiFreightXML.msedi_imports.customs.importer_address.append(
                    ImporterAddress1)
                # multiFreightXML.msedi_imports.customs.importer_address.append(
                #     ImporterAddress2)
                multiFreightXML.msedi_imports.customs.importer_county = ImporterCounty
                multiFreightXML.msedi_imports.customs.importer_country = ImporterCountry
                multiFreightXML.msedi_imports.customs.importer_vatregn = CnsgeTid
                multiFreightXML.msedi_imports.customs.agent_name = 'CARGO OVERSEAS LIMITED'
                multiFreightXML.msedi_imports.customs.agent_address.append('FLOATS ROAD')
                multiFreightXML.msedi_imports.customs.agent_address.append('ROUNDTHORN IND EST')
                multiFreightXML.msedi_imports.customs.agent_county = 'M25 9NJ'
                multiFreightXML.msedi_imports.customs.agent_country = 'GB'
                multiFreightXML.msedi_imports.customs.agent_vatregn = 'GB548600440000'
                multiFreightXML.msedi_imports.customs.agent_tel = '0161 498 6111'
                multiFreightXML.msedi_imports.customs.pkgs = PiecesTotal
                #multiFreightXML.msedi_imports.customs.gross_weight = GWTotal           #not needed as per conv with damian
                multiFreightXML.msedi_imports.customs.port_loading = PortLoading
                multiFreightXML.msedi_imports.customs.country_dispatch = CountryDespatch
                multiFreightXML.msedi_imports.customs.transport_type = TransportType
                multiFreightXML.msedi_imports.customs.port_import = PortImport if InvLinked else "Felixstowe"
                multiFreightXML.msedi_imports.customs.port_import_code = ukPortCode if InvLinked else "FXT"
                multiFreightXML.msedi_imports.customs.wunit = 'KGS'
                multiFreightXML.msedi_imports.customs.portcode = ukPortCode if InvLinked else "FXT"
                multiFreightXML.msedi_imports.customs.inventory = inventory if inventory else ""
                # multiFreightXML.msedi_imports.customs.edi_cdec_itm_ai.item_no = '0'       £ header level ai not required as on item 1level
                # multiFreightXML.msedi_imports.customs.edi_cdec_itm_ai.ai_no = '1'
                # multiFreightXML.msedi_imports.customs.edi_cdec_itm_ai.item_ai_stmt = ItemAiStmt



                globalDutyTest = None     #test if there are any items in the commodity code list that have duty. If so set the dutytest to True
                x = 1
                for item in whatList:
                    hsCode = str(item['Commodity code (10)'])
                    #print(hsCode)
                    commodityNumber = str(item['Commodity code (10)'])
                    #print(commodityNumber) #needs to be outside the eu
                    cooItemTest = str(item['CountryOfOrigin'])
                    euPreference = False
                    cooInEu = cooItemTest in inEuCoo
                    hsDetails = getHsDetails(commodityNumber)
                    dutyRate = hsDetails['dutyRate']
                    print(dutyRate)
                    if dutyRate != "0.00" and not cooInEu:
                        globalDutyTest = True
                    elif dutyRate != "0.00" and cooInEu and not euPreference:   
                        globalDutyTest = True    
                    x+=1
                print(globalDutyTest)
                ItemNo = 1
                for item in whatList:
                    commodityNumber = str(item['Commodity code (10)'])
                    # hsTranslatedCommodityNumber = hs10Translate(commodityNumber)
                    # if hsTranslatedCommodityNumber: ##translate the comm code if there is a match in the hs10 codes list
                    #     commodityNumber = hsTranslatedCommodityNumber
                    #dutyRate = callGovApiAndgetDutyRate(commodityNumber)       ##previous gov api call
                    hsDetails = getHsDetails(commodityNumber)
                    dutyRate = hsDetails.get("dutyRate")      ##new internal cache data
                    #vatRates = callIntCacheAndGetVATRates(commodityNumber)
                    euPreference = True
                    ##patch packages if NA
                    packageTest = str(item['ItemPackageTypeCode']) 
                    if packageTest == "NA":
                        packageType = "PK"
                    else: 
                        packageType = str(item['ItemPackageTypeCode'])     
                    supplementaryUnits = hsDetails.get('supplementaryUnits')
                    # if euPreference == None:
                    #     euPreference = True 
                    # print(vatRates)
                    # print(type(vatRates))
                    try:
                        vatStandard = hsDetails.get('vatStandard')
                        vatZero = hsDetails.get('vatZero')
                        vatA = hsDetails.get('vatA')
                    except Exception as e:
                        logger.warning(f" {e.__class__.__name__}: {e} - couldnt get vat ")
                        vatStandard = False
                        vatZero = False
                        vatA = False
                        logger.exception(e)
                        sentry_sdk.capture_exception(e) 

                    coo = str(item['CountryOfOrigin'])
                    ##coo test:
                    cooValid  = False
                    for x in countryList:
                        if x['value'] == coo:
                            cooValid  = True
                    
                    if not cooValid:
                        contentsEmail = f"Please note your reference {customerReference} contains an incorrect country Code - {coo}. <br/><br/>Please contact us urgently so we can transmit your entry." 
                        #acemail.send(to="export.department@electrolux.de", cc=ace@forwarding.digital, subject=f"{cominvref} contains unmapped HS code", contents=genEmail(contentsEmail))
                        jhmail.send(to="jheavyside@trilogyfreight.com", subject=f"{customerReference} contains an incorrect country of origin - {coo}", contents=genEmail(contentsEmail))
                        jhmail.send(to="howden@cargo-overseas.co.uk", subject=f"{customerReference} contains an incorrect country of origin - {coo}", contents=genEmail(contentsEmail))
                        try:
                            os.replace(from_path, error_path_failed_hs8)
                        except Exception as e:
                            logger.warning(f" {e.__class__.__name__}: {e} - couldnt move to error folder ")
                        failHs8Test = True
                    inEu = coo in inEuCoo

                    #if deferredAccounting:    #going forward                
                    #if not dateTest and deferredAccounting:   #prior to 1st                 
                    if deferredAccounting:   #after brexit
                        if vatStandard:             #this sets the vat in the tax lines below
                            MopCodeV = "G"      # if before jan, if deferment ="F", if FAS = "D", if they select NA put "D"
                            taxRate = "S"
                        else:
                            if vatA:
                                MopCodeV = "G"
                                taxRate = 'A'
                            else:
                                if vatZero:
                                    MopCodeV = None    
                                    taxRate = 'Z'
                                else:
                                    MopCodeV = None
                                    taxRate = None   
                    else:
                        MopCodeV = "F" if FirDanPfx == "B" else "D"
                        if vatStandard:             #before bresit
                            taxRate = "S"
                        else:
                            if vatA:
                                taxRate = 'A'
                            else:
                                if vatZero:
                                    taxRate = 'Z'
                                    MopCodeV = ""
                                else:
                                    taxRate = None   

        
                    ItemNoS = str(ItemNo)
                    CusItems = mflib.CustomsItem()
                    
                    if euPreference:    
                        if globalDutyTest:  #if any items have duty then add an additional document to the current logic. Use the pre looped globalDutytest. if they are not in the eu just keep the current doc
                            if inEu:
                                if dutyRate != "0.00":      
                                    doc1 = mflib.EDICdecItmDoc()                        #we do not need this if dutyRate is greater than 0
                                    doc1.item_doc_code = "U110" if inEu else ItemDocCode
                                    doc1.item_doc_qty = '0'
                                    doc1.item_doc_status = 'AE'
                                    doc1.item_no = ItemNoS                 
                                    doc1.doc_no = '1'
                                    doc1.item_doc_ref = InvNr if inEu else ''
                                    CusItems.edi_cdec_itm_doc.append(doc1)
                                    itemsDutyTest.append(dutyTrue)      ##dutytest to check if need to remove the deferment account line below
                                    doc2 = mflib.EDICdecItmDoc() 
                                    doc2.item_doc_code = ItemDocCode   #if we are in the eu we need to add the 2nd document in
                                    doc2.item_doc_qty = '0'
                                    doc2.item_doc_status = 'AE'
                                    doc2.item_no = ItemNoS                 
                                    doc2.doc_no = '2'    
                                    CusItems.edi_cdec_itm_doc.append(doc2) 
                                elif dutyRate == "0.00": ## if there are any other items with duty add the below document in
                                    doc1 = mflib.EDICdecItmDoc()  
                                    doc1.item_doc_code = ItemDocCode
                                    doc1.item_doc_qty = '0'
                                    doc1.item_doc_status = 'AE'
                                    doc1.item_no = ItemNoS                 
                                    doc1.doc_no = '1'
                                    CusItems.edi_cdec_itm_doc.append(doc1)
                            else:
                                if dutyRate != "0.00":
                                    doc1 = mflib.EDICdecItmDoc()                        #we do not need this if dutyRate is greater than 0
                                    doc1.item_doc_code = "U110" if inEu else ItemDocCode
                                    doc1.item_doc_qty = '0'
                                    doc1.item_doc_status = 'AE'
                                    doc1.item_no = ItemNoS                 
                                    doc1.doc_no = '1'
                                    doc1.item_doc_ref = InvNr if inEu else ''
                                    CusItems.edi_cdec_itm_doc.append(doc1)
                                    itemsDutyTest.append(dutyTrue)      ##dutytest to check if need to remove the deferment account line below
                                elif dutyRate == "0.00" and globalDutyTest: ## if there are any other items with duty add the below document in
                                    doc1 = mflib.EDICdecItmDoc()  
                                    doc1.item_doc_code = ItemDocCode
                                    doc1.item_doc_qty = '0'
                                    doc1.item_doc_status = 'AE'
                                    doc1.item_no = ItemNoS                 
                                    doc1.doc_no = '1'
                        else:
                            if inEu:
                                if dutyRate != "0.00":
                                    doc1 = mflib.EDICdecItmDoc()                        #we do not need this if dutyRate is greater than 0
                                    doc1.item_doc_code = "U110" if inEu else ItemDocCode
                                    doc1.item_doc_qty = '0'
                                    doc1.item_doc_status = 'AE'
                                    doc1.item_no = ItemNoS                 
                                    doc1.doc_no = '1'
                                    doc1.item_doc_ref = InvNr if inEu else ''
                                    CusItems.edi_cdec_itm_doc.append(doc1)
                                    itemsDutyTest.append(dutyTrue)


                    else: 
                        if globalDutyTest:
                            doc1 = mflib.EDICdecItmDoc()                        #we only need this if dutyRate is greater than 0 on an item
                            doc1.item_doc_code =  ItemDocCode
                            doc1.item_doc_qty = '0'
                            doc1.item_doc_status = 'AE'
                            doc1.item_no = ItemNoS                 
                            doc1.doc_no = '1'
                            CusItems.edi_cdec_itm_doc.append(doc1)                         

                                
                        else:
                            if dutyRate != "0.00":     ##original logic 
                                doc1 = mflib.EDICdecItmDoc()                        #we only need this if dutyRate is greater than 0 on an item
                                doc1.item_doc_code =  ItemDocCode
                                doc1.item_doc_qty = '0'
                                doc1.item_doc_status = 'AE'
                                doc1.item_no = ItemNoS                 
                                doc1.doc_no = '1'
                                CusItems.edi_cdec_itm_doc.append(doc1)
                        
                        
                        
                        
                          ##original logic      
                        # if dutyRate != "0.00":     
                        #     doc1 = mflib.EDICdecItmDoc()                        #we only need this if dutyRate is greater than 0 on an item
                        #     doc1.item_doc_code =  ItemDocCode
                        #     doc1.item_doc_qty = '0'
                        #     doc1.item_doc_status = 'AE'
                        #     doc1.item_no = ItemNoS                 
                        #     doc1.doc_no = '1'
                        #     CusItems.edi_cdec_itm_doc.append(doc1)
                        #     itemsDutyTest.append(dutyTrue) 

                    CusItems.commodity_desc =  ""             #needs to be from the items array
                    CusItems.item_no = ItemNoS
                    CusItems.qty_code = QtyCode
                    CusItems.pkgs = PiecesTotal
                    aiStat1 = mflib.EDICdecItmAI()
                    aiStat1.item_no = ItemNoS
                    aiStat1.ai_no = '1'
                    aiStat1.item_ai_stmt = ItemAiStmt
                    CusItems.edi_cdec_itm_ai.append(aiStat1)
                    # if not dateTest:    # and dateTest2:      ## temporary extra clause we need to add into all ai level entries
                    aiStat2 = mflib.EDICdecItmAI()
                    aiStat2.item_no = ItemNoS
                    aiStat2.ai_no = '2'
                    aiStat2.item_ai_stmt = "GEN53"
                    aiStat2.item_ai_stmt_txt = "2021"
                    CusItems.edi_cdec_itm_ai.append(aiStat2)
                    CusItems.edi_cdec_itm_pkg.item_no = ItemNoS
                    CusItems.edi_cdec_itm_pkg.pkg_no = '1'
                    CusItems.edi_cdec_itm_pkg.pkg_kind = packageType  ##if
                    bulkPackagestest = "PK" in bulkPackages
                    CusItems.edi_cdec_itm_pkg.pkg_count = str(item['ItemPackageQuantity']) if not bulkPackagestest else "" 
                    CusItems.edi_cdec_itm_pkg.pkg_marks_lng = '1'
                    CusItems.edi_cdec_itm_pkg.pkg_marks = 'AS ADDRESSED'
                    CusItems.edi_cdec_itm_pdc.item_no = ItemNoS
                    CusItems.edi_cdec_itm_pdc.pdc_no = '1'
                    CusItems.edi_cdec_itm_pdc.prev_doc_class = PrevDocClass
                    CusItems.edi_cdec_itm_pdc.prev_doc_ref = InvNr
                    CusItems.edi_cdec_itm_pdc.prev_doc_type = PrevDocType
                    TaxItems1 = mflib.EDICdecItmTax()
                    TaxItems1.mop_code = MopCodeV     
                    TaxItems1.item_no = ItemNoS
                    TaxItems1.tax_no = '1'
                    TaxItems1.tax_rate_id = taxRate
                    TaxItems1.tty_code = 'B00'
                    CusItems.edi_cdec_itm_tax.append(TaxItems1)
                    if dutyRate != "0.00":
                        Taxitems2 = mflib.EDICdecItmTax()
                        Taxitems2.item_no = ItemNoS
                        Taxitems2.mop_code = "" if inEu and euPreference else MopCodeD    # don't need if duty == "0.00". If it is dutyable but in the eu dont show mop
                        Taxitems2.tax_no = '2'
                        Taxitems2.tax_rate_id = "A" if inEu and euPreference else "F"   ##only use A if it is in the eu and they chose eu preference..ie true
                        Taxitems2.tty_code = "A00"
                        CusItems.edi_cdec_itm_tax.append(Taxitems2)
                    multiFreightXML.msedi_imports.customs.customs_item.append(
                        CusItems)
                    EdiCdecItem = mflib.EDICdecItm()
                    EdiCdecItem.cpc = "4000000"
                    ##clean descriptions
                    descriptionRaw = str(item['GoodsDescription']) 
                    descriptionStripped = re.sub(r'\W+', ' ', descriptionRaw)
                    descriptionFormatted = str(unicodedata.normalize("NFD", descriptionStripped).encode('WINDOWS-1252', 'ignore'))[2:-2]
                    EdiCdecItem.gds_desc =  descriptionFormatted                  
                    EdiCdecItem.item_net_mass = str(item['NetMass'])
                    EdiCdecItem.item_no = ItemNoS
                    EdiCdecItem.item_orig_cntry = str(item['CountryOfOrigin'])
                    supplementaryUnitsValue = str(item['SupplementaryUnits'])
                    # if supplementaryUnits:    ##supplementary units logic as agreed with gregg 02/11/21
                    #     EdiCdecItem.item_supp_units = supplementaryUnitsValue if supplementaryUnitsValue else str(item['ItemPackageQuantity'])
                    EdiCdecItem.item_prc_ac = str(item['ItemPrice'])
                    if dutyRate != "0.00":
                        EdiCdecItem.preference = "300" if inEu and euPreference else Preference  #change the preference to 300 if in the Eu and eupreference = true
                    else:
                        EdiCdecItem.preference = Preference
                    EdiCdecItem.taric_cmdty_code = commodityNumber
                    EdiCdecItem.val_mthd_code = ValMthdCode if dutyRate != "0.00" else ""                   #don't need if duty is "0.00"
                    if inEu and euPreference:
                        EdiCdecItem.val_mthd_code = ""      #take out if in the Eu regardless if there is a dutyline
                    if globalDutyTest:
                        EdiCdecItem.val_mthd_code = ValMthdCode
                    EdiCdecItem.val_adjt_code = ValAdjtCode
                    multiFreightXML.msedi_imports.customs.edi_cdec_itm.append(
                        EdiCdecItem)
                    ItemNo += 1

                #   EDI CDEC ITEM - list

                #   EDI_CDEC
                multiFreightXML.msedi_imports.edi_cdec = mflib.EDICdec()
                multiFreightXML.msedi_imports.edi_cdec.tdr_own_ref_ent = 'replace-job-disp'
                multiFreightXML.msedi_imports.edi_cdec.declt_rep = DecltRep
                multiFreightXML.msedi_imports.edi_cdec.disp_cntry = DispCntry
                multiFreightXML.msedi_imports.edi_cdec.decln_type = DeclnType
                multiFreightXML.msedi_imports.edi_cdec.fir_dan = FirDan
                multiFreightXML.msedi_imports.edi_cdec.fir_dan_pfx = FirDanPfx
                if Mode == "Road":
                    multiFreightXML.msedi_imports.edi_cdec.gds_locn_code = "GB" + ukPortCode    #for roadfreight need the location regardless of invlinked
                else:    
                    multiFreightXML.msedi_imports.edi_cdec.gds_locn_code = "GB" + ukPortCode if InvLinked else "GBMAN"
                # multiFreightXML.msedi_imports.edi_cdec.pla_ldg_code = ''#Not sure what this is
                multiFreightXML.msedi_imports.edi_cdec.tot_pkgs = PiecesTotal
                multiFreightXML.msedi_imports.edi_cdec.trpt_cntry = DispCntry
                multiFreightXML.msedi_imports.edi_cdec.trpt_id = TrptId
                multiFreightXML.msedi_imports.edi_cdec.trpt_mode_code = TrptModeCode
                multiFreightXML.msedi_imports.edi_cdec.cnsge_city = CnsgeCity
                multiFreightXML.msedi_imports.edi_cdec.cnsge_name = CnsgeName
                multiFreightXML.msedi_imports.edi_cdec.cnsge_postcode = CnsgePostcode
                multiFreightXML.msedi_imports.edi_cdec.cnsge_street = CnsgeStreet
                multiFreightXML.msedi_imports.edi_cdec.cnsge_cntry = CnsgeCntry
                multiFreightXML.msedi_imports.edi_cdec.cnsge_tid = CnsgeTid
                multiFreightXML.msedi_imports.edi_cdec.cnsgr_city = CnsgrCity
                multiFreightXML.msedi_imports.edi_cdec.cnsgr_cntry = CnsgrCntry
                multiFreightXML.msedi_imports.edi_cdec.cnsgr_name = CnsgrName
                multiFreightXML.msedi_imports.edi_cdec.cnsgr_postcode = CnsgrPostCode
                multiFreightXML.msedi_imports.edi_cdec.cnsgr_street = CnsgrStreet
                #multiFreightXML.msedi_imports.edi_cdec.cnsgr_tid = CnsgrTid            #damian says not needed
                multiFreightXML.msedi_imports.edi_cdec.declt_city = DecltCity
                multiFreightXML.msedi_imports.edi_cdec.declt_cntry = DecltCntry
                multiFreightXML.msedi_imports.edi_cdec.declt_name = DecltName
                multiFreightXML.msedi_imports.edi_cdec.declt_postcode = DecltPostcode
                multiFreightXML.msedi_imports.edi_cdec.declt_street = DecltStreet
                multiFreightXML.msedi_imports.edi_cdec.declt_tid = DecltTid
                multiFreightXML.msedi_imports.edi_cdec.intd_arr_dtm = IntdArrDtm 
                multiFreightXML.msedi_imports.edi_cdec.inv_crrn = str(Cur)
                multiFreightXML.msedi_imports.edi_cdec.inv_tot_ac = Total
                multiFreightXML.msedi_imports.edi_cdec.decln_ucr = DucrS

                ##Financials depending on invoice terms additional fields
                #print("731")

                # if Terms == "EXW":    
                #     freightInsCoststoUkBorder = modelData['entry']['header']['freightInsCostsUkPort']
                #     freightInsCoststoUkBorderCurrency = modelData['entry']['header']['freightInsCostsUkPortCurrency']
                #     costsUkBorderToDoorCurrency = modelData['entry']['header']['costsFromUKBorderToDoorCurrency']
                #     costsUkBorderToDoor = modelData['entry']['header']['costsFromUKBorderToDoor']
                #     multiFreightXML.msedi_imports.edi_cdec.frgt_chge_ac = str(freightInsCoststoUkBorder)
                #     multiFreightXML.msedi_imports.edi_cdec.frgt_chge_crrn = freightInsCoststoUkBorderCurrency
                #     multiFreightXML.msedi_imports.edi_cdec.vat_adjt_ac = str(costsUkBorderToDoor)
                #     multiFreightXML.msedi_imports.edi_cdec.vat_adjt_crrn = costsUkBorderToDoorCurrency
                #     if Mode == "Air":
                #         multiFreightXML.msedi_imports.edi_cdec.farp_code = PortLoading[2:5]
                #         freightInsCoststoUkBorder = modelData['entry']['header']['freightInsCostsUkPort']
                #         #freightInsCoststoUkBorderCurrency = modelData['entry']['header']['freightInsCostsUkPortCurrency']
                #         multiFreightXML.msedi_imports.edi_cdec.atrpt_cost_ac = str(freightInsCoststoUkBorder)

                # elif Terms == "CIF":
                #     costsUkBorderToDoor = modelData['entry']['header']['costsFromUKBorderToDoor']
                #     costsUkBorderToDoorCurrency = modelData['entry']['header']['costsFromUKBorderToDoorCurrency']
                #     multiFreightXML.msedi_imports.edi_cdec.vat_adjt_ac = costsUkBorderToDoor
                #     multiFreightXML.msedi_imports.edi_cdec.vat_adjt_crrn = costsUkBorderToDoorCurrency

                # elif Terms == "FOB":
                #     freightInsCoststoUkBorder = modelData['entry']['header']['fICPDUB']
                #     freightInsCoststoUkBorderCurrency = modelData['entry']['header']['fICPDUBCurrency']
                #     costsUkBorderToDoorCurrency = modelData['entry']['header']['costsFromUKBorderToDoorCurrency']
                #     costsUkBorderToDoor = modelData['entry']['header']['costsFromUKBorderToDoor']
                #     multiFreightXML.msedi_imports.edi_cdec.frgt_chge_ac = str(freightInsCoststoUkBorder)
                #     multiFreightXML.msedi_imports.edi_cdec.frgt_chge_crrn = freightInsCoststoUkBorderCurrency
                #     multiFreightXML.msedi_imports.edi_cdec.vat_adjt_ac = str(costsUkBorderToDoor)
                #     multiFreightXML.msedi_imports.edi_cdec.vat_adjt_crrn = costsUkBorderToDoorCurrency
                #     if Mode == "Air":
                #         multiFreightXML.msedi_imports.edi_cdec.farp_code = PortLoading[2:5]
                #         freightInsCoststoUkBorder = modelData['entry']['header']['freightInsCostsUkPort']
                #         #freightInsCoststoUkBorderCurrency = modelData['entry']['header']['freightInsCostsUkPortCurrency']
                #         multiFreightXML.msedi_imports.edi_cdec.atrpt_cost_ac = str(freightInsCoststoUkBorder)

                if deferredAccounting:
                    if not itemsDutyTest and FirDanPfx == "B":      #if there is no duty on any items remove the deferment account as there is nothing to pay
                        multiFreightXML.msedi_imports.edi_cdec.fir_dan = None
                        multiFreightXML.msedi_imports.edi_cdec.fir_dan_pfx = None

                if not itemsDutyTest and internalDeferment == True:    #if there is no duty on any items remove the deferment account as there is nothing to pay
                    multiFreightXML.msedi_imports.edi_cdec.fir_dan = None
                    multiFreightXML.msedi_imports.edi_cdec.fir_dan_pfx = None





                NoR = len(whatList)

                if  NoR < 100 and callType =="L":
                    MFXmlFile = temp + "/" + portalID + "-" + str(InvNr.replace("/", "")) + ".xml"
                    #try:
                    MFFile = open(MFXmlFile, "w")           # OPen the multifreight file
                    multiFreightXML.xml_type = Direction    # output the multifreight xml
                    mfxmlout = multiFreightXML.to_xml()  
                    logger.info("\n" + mfxmlout)
                    #mfxmloutdict = multiFreightXML.to_dict()
                    MFFile.write(mfxmlout)
                    MFFile.close()
                    # if entryJson:
                    #     try:
                    #         jsonFilePath = temp + "/" + "json-" + portalID + ".json"
                    #         jsonFile = open(jsonFilePath, "w") 
                    #         jsonFile.write(entryJson)
                    #         jsonFile.close()
                    #         jhcargomail.send(to="jheavyside@trilogyfreight.com", subject = f"{AddressCode} - succesful import" , contents = "congrats. import attached", attachments = [MFXmlFile, jsonFilePath] )
                    #         os.remove(jsonFilePath)
                    #     except Exception as e:
                    #         logger.warning(f" {e.__class__.__name__}: {e} - counldnt generate the json file attachment ")
                    #         logger.exception(e)
                    #         sentry_sdk.capture_exception(e)     
                    # else:
                    try:
                        jhmail.send(to="jheavyside@trilogyfreight.com", subject = f"{AddressCode} - succesful DAF Auto EDI in" , contents = "Processed DAF EDI in", attachments = MFXmlFile )
                        jhmail.send(to="howden@cargo-overseas.co.uk", subject = f"{AddressCode} - succesful DAF Auto EDI in" , contents = "Processed DAF EDI in", attachments = MFXmlFile )
                    except Exception as e:
                        logger.error(f"file_name {e.__class__.__name__}: {e} error on sending an email out")
                        pass


                    mfOutLoc = tomultifreight #+ "/" + portalID + ".xml"
                    shutil.move(MFXmlFile, mfOutLoc)
                    logger.info(file_name + " Created The Multifreight XML")

            if failHs8Test == False:
                try:
                    shutil.move(from_path, outFullPath)
                except Exception as e:
                    logger.error(f"file_name {e.__class__.__name__}: {e} error on trying to move. someone already moved")
                    pass    
              

            # else:
            #     logger.info(f"elec ref {headerInvNumber} created no entry. Contains unmapped hs codes")

        # except Exception as e:
        #         logger.error(f"file_name {e.__class__.__name__}: {e} Has not been Processed and moved to the error folder")
        #         os.replace(from_path, error_path)
        #         pass

if __name__ == '__main__':
    w = Watcher()
    w.run()