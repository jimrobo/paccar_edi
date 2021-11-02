from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String, DateTime, Date, ForeignKey, JSON, BOOLEAN, Numeric
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker
from datetime import date
import pprint
import sentry_sdk
from sentry_sdk.integrations.redis import RedisIntegration
import json

with open("config.json") as config_file:
    config_data = json.load(config_file)

##set the db data
dbUser = config_data["dbUser"]
dbPassword = config_data["dbPass"]


try:
    #engine = create_engine("mysql+pymysql://doadmin:fcmwhnq0mjjyh863@db-mysql-cargoedi-do-user-7435356-0.a.db.ondigitalocean.com:25060/ace_portal", pool_pre_ping=True, pool_size=30, max_overflow=20, echo=False)
    engine = create_engine(f"mysql+pymysql://{dbUser}:{dbPassword}@db-mysql-cargoedi-do-user-7435356-0.a.db.ondigitalocean.com:25060/ace_portal", pool_pre_ping=True, pool_size=5, pool_recycle=25200, max_overflow=10, echo=False)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()
except Exception as e:
            print(f" {e.__class__.__name__}: {e}  - Connecting to DB through an error") 
            sentry_sdk.capture_exception(e)    

##set up the trilogy db connection:
try:
    #engine = create_engine("mysql+pymysql://doadmin:fcmwhnq0mjjyh863@db-mysql-cargoedi-do-user-7435356-0.a.db.ondigitalocean.com:25060/ace_portal", pool_pre_ping=True, pool_size=30, max_overflow=20, echo=False)
    engineTril = create_engine(f"mysql+pymysql://doadmin:k6gunbm1flttxcv0@db-mysql-lon1-08727-do-user-7435356-0.b.db.ondigitalocean.com:25060/defaultdb", pool_pre_ping=True, pool_size=5, pool_recycle=25200, max_overflow=10, echo=False)
    SessionTril = sessionmaker(bind=engineTril)
    sessionTril = SessionTril()
except Exception as e:
            print(f" {e.__class__.__name__}: {e}  - Connecting to TRILDB through an error") 
            sentry_sdk.capture_exception(e)                

engineDev = create_engine("mysql+pymysql://doadmin:fcmwhnq0mjjyh863@db-mysql-cargoedi-do-user-7435356-0.a.db.ondigitalocean.com:25060/jhdev", echo=False)
SessionDev = sessionmaker(bind=engineDev)
sessionDev = SessionDev()


# with engine.connect() as conn:
#     result = conn.execute(text("SELECT * FROM users"))
#     for row in result:
#         print(row)

class users(Base):
    __tablename__ = 'users'

    id = Column(String(25), primary_key=True)
    sub = Column(String(30), nullable=False)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)
    ftpFolder = Column(String, nullable=False)
    accountId = Column(String(25), ForeignKey('accounts.id'), nullable=False)
    email = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)

    # accounts = relationship("accounts", back_populates="users")

    def __repr__(self):
        return f"users(id={self.id!r}, email = {self.email!r}, country = {self.country!r} , sub={self.sub!r}, createdAt={self.createdAt!r}, updatedAt={self.updatedAt!r}, ftpFolder{self.ftpFolder!r}, accountId={self.accountId!r})"


class accounts(Base):
    __tablename__ = 'accounts'

    id = Column(String(25), ForeignKey('users.accountId'), primary_key=True)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)
    addressCode = Column(String, nullable=False)
    subscriptionTier = Column(String, nullable=False)


    def __repr__(self):
        return f"accounts(id={self.id!r}, createdAt={self.createdAt!r}, updatedAt={self.updatedAt!r}, addressCode = {self.addressCode!r}, subscriptionTier={self.subscriptionTier!r})"


class jobs(Base):
    __tablename__ = 'jobs'

    id = Column(String(25), primary_key=True)
    #mfdata = Column(JSON, nullable=False)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)
    clearanceDate = Column(DateTime, nullable=False)
    recId = Column(String(255), nullable=False)
    jobDate = Column(Date, nullable=False)
    mfRef = Column(String(255), nullable=False)
    clearanceRoute = Column(String(255), nullable=False)
    entryNumber = Column(String(255), nullable=False)
    docs = Column(JSON, nullable=False)
    status = Column(String(255), nullable=False)
    statusDate = Column(Date, nullable=False)
    accountCode = Column(String(255), nullable=False)
    entryCreated = Column(DateTime, nullable=False)
    mrn = Column(String(255), nullable=True)
    ucr = Column(String(255), nullable=True)
    jobs3RouteCode = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)


    def __repr__(self):
        return f"jobs(id={self.id!r}, createdAt={self.createdAt!r}, updatedAt={self.updatedAt!r}, clearanceDate={self.clearanceDate!r}, recId{self.recId!r}, jobDate={self.jobDate!r}), mfRef={self.mfRef!r}, clearanceRoute = {self.clearanceRoute!r}, entryNumber = {self.entryNumber!r}, docs = {self.docs!r}, status={self.status!r}, statusDate={self.statusDate!r}, accountCode={self.accountCode!r}, entryCreated={self.entryCreated!r}, mrn = {self.mrn!r}, ucr = {self.ucr!r}, jobs3RouteCode = {self.jobs3RouteCode!r}, country = {self.country!r}"        



class ports(Base):
    __tablename__ = 'ports'

    id = Column(String(25), primary_key=True)
    portcode = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    countryCode = Column(String(255), nullable=False)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)
    ukPortCode = Column(String(255), nullable=True)

    def __repr__(self):
        return f"ports(id={self.id!r}, portcode={self.portcode!r}, name={self.name!r}, countryCode={self.countryCode!r}, createdAt{self.createdAt!r}, updatedAt={self.updatedAt!r})"
    

class airports(Base):
    __tablename__ = 'airports'

    id = Column(String(25), primary_key=True)
    ident = Column(String(255), nullable=False)
    type = Column('type_', String(255), nullable=False)
    name = Column(String(255), nullable=False)
    continent = Column(String(255), nullable=False)
    iso_country = Column(String(255), nullable=False)
    iata_code = Column(String(255), nullable=False)
    international_code = Column(String(255), nullable=False)
    iso_region = Column(String(255), nullable=False)
    municipality = Column(String(255), nullable=False)
    scheduled_service = Column(String(255), nullable=False)
    gps_code = Column(String(255), nullable=False)
    local_code = Column(String(255), nullable=False)
    lattitude_deg = Column(Numeric(10), nullable=False)
    longitude_deg = Column(Numeric(11), nullable=False)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"airports(id={self.id!r}, ident={self.ident!r}, type={self.type_!r}, name={self.name!r}, continent{self.continent!r}, isoCountry={self.iso_country!r}, createdAt{self.createdAt!r}, updatedAt={self.updatedAt!r})"
        
    

class entries(Base):
    __tablename__ = 'entries'

    id = Column(String(25), primary_key=True)
    accountId = Column(String(25), ForeignKey('accounts.id'), nullable=False)
    userId = Column(String(25), ForeignKey('users.id'), nullable=False)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)
    entryData = Column(DateTime, nullable=False)
    jobId = Column(String(25), ForeignKey('jobs.id'), nullable=True)
    entryType = Column(String(255), nullable=False)
    country = Column(String(255), nullable=True)
    declarationId = Column(String(255), nullable=True)

    def __repr__(self):
        return f"entries(id={self.id!r}, declarationId = {self.declarationId!r}, accountID={self.accountId!r}, userId={self.userId!r}, createdAt={self.createdAt!r}, updatedAt{self.updatedAt!r}, entryData={self.entryData!r}, jobId={self.jobId!r}, entryType={self.entryType!r}), country = {self.country!r}"
        
class notifications(Base):
    __tablename__ = 'notifications'

    id = Column(String(25), primary_key=True)
    jobId = Column(String(25), ForeignKey('jobs.id'), nullable=False)
    createdAt = Column(DateTime, nullable=True)
    updatedAt = Column(DateTime, nullable=True)
    n1 = Column(String(255), nullable=True)
    n2 = Column(String(255), nullable=True)
    n3 = Column(String(255), nullable=True)
    n4 = Column(String(255), nullable=True)
    n5 = Column(String(255), nullable=True)
    

    def __repr__(self):
        return f"id(id={self.id!r}, jobID={self.jobId!r}, createdAt={self.createdAt!r}, updatedAt{self.updatedAt!r}, n1={self.n1!r}, n2={self.n2!r}, n3={self.n3!r}), n4={self.n4!r}), n5={self.n5!r})"


class ncts(Base):
    __tablename__ = 'ncts'

    id = Column(String(25), primary_key=True)
    jobId = Column(String(25), ForeignKey('jobs.id'), nullable=False)
    createdAt = Column(DateTime, nullable=True)
    updatedAt = Column(DateTime, nullable=True)
    mrn = Column(String(255), nullable=True)
    lrn = Column(String(255), nullable=True)
    consignor = Column(String(255), nullable=True)
    consignee = Column(String(255), nullable=True)
    office = Column(String(255), nullable=True)
    nctsData = Column(JSON, nullable=False)
    status = Column(String(255), nullable=True)
    departureId = Column(String(255), nullable=True)
    accountId = Column(String(255), nullable=True)
    userId = Column(String(255), nullable=True)
    guaranteeAmount = Column(String(255), nullable=True)
    custReference = Column(String(255), nullable=True)
    

    def __repr__(self):
        return f"id(id={self.id!r}, accountId = {self.accountId!r}, userId = {self.userId!r}, jobID={self.jobId!r}, createdAt={self.createdAt!r}, updatedAt={self.updatedAt!r}, mrn{self.mrn!r}, lrn={self.lrn!r}, consignor={self.consignor!r}, consignee={self.consignee!r}), office={self.office!r}), status={self.status!r}), departureId = {self.departureId!r}"

##add trilogydb class

class quotes(Base):
    __tablename__ = 'quotes'

    id = Column(String(25), primary_key=True)
    customer = Column(String(255), nullable=False)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)
    weight = Column(String(255), nullable=False)
    volume = Column(String(25), nullable=False)
    postCode1 = Column(String(25), nullable=False)
    postCode2 = Column(String(25), nullable=False)
    date = Column(Date, nullable=False)
    dayOfWeek = Column(String(25), nullable=False)


    def __repr__(self):
        return f"User(id={self.id!r}, postCode1={self.postCode1!r}, postCode2 = {self.postCode2!r},customer={self.customer!r}, createdAt={self.createdAt!r}, updatedAt={self.updatedAt!r}, weight{self.weight!r}, volume={self.volume!r})"    


class custrans(Base):
    __tablename__ = 'custrans'

    id = Column(String(25), primary_key=True)
    accountId = Column(String(25), ForeignKey('accounts.id'), nullable=False)
    status = Column(String(255), nullable=False)
    client_name = Column(String(255), nullable=False)
    client_id = Column(String(255), nullable=False)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)


    def __repr__(self):
        return f"custrans(id={self.id!r}, clientId = {self.clientId!r}, accountId={self.accountId!r}, createdAt={self.createdAt!r}, updatedAt={self.updatedAt!r}, status = {self.status!r}, clientName = {self.clientName!r})"



# print(select(jobs).where(jobs.accountCode=="FLEX034"))  
# jobsQuery = session.query(jobs) \
#     .filter(jobs.createdAt == date(2020, 1, 9)) \
#     .all()

# jobsind = session.query(jobs).filter(jobs.accountCode == 'FLEX043')
# print(jobsind.count())

# jobsind = session.query(jobs).filter(jobs.accountCode == 'FLEX043').limit(50)
# # print(jobsind.count())
# for jobs in jobsind:
#     #  print(jobs.mfdata['ISLEDI']['Tables']["job-hdr"]["job-disp"])
#      print(jobs.mfRef)

# customsDocCodes = {
#     "CUSC88": "Import entry acceptance C88",
#     "CUSH2": "DTI H2",
#     "CUSE2": "DTI-E2",
#     "CUSE2AMD": "DTI-E2-AMD ammended E2",
#     "CUSE9": "DTI – E9 - Payment required by fas",
#     "CUSN6": "DTI – N6 Customs query advice",
#     "CUSN4": "DTI -N4 Import cancellation approval advice",
#     "CUSFSN": "FSN Status report",
#     "CUSTC3": "Export Entry acceptance (TC3)",
#     "CUSP2": "DTI-P2 - pre entry acceptance",
#     "CUSX2XH": "DTI X2 XH - Accepted by Airline",
#     "CUSS8": "DTI-S8 - Goods Departure",
#     "CUSS6": "DTI-S6 - Customs query advice",
#     "CUSX6": "DTI-X6 - Export entry progress advice",
#   }


# portalId = "ckh6cj4jq0000xmh2a3se5qe5"
# entrysearch = session.query(entries).filter(entries.id == portalId)
# #print(entrysearch[0].jobId)
# jobtosearchfor = (entrysearch[0].jobId)
# jobsearch = session.query(jobs).filter(jobs.id == jobtosearchfor)
# #print(jobsearch[0])
# searchedJob = jobsearch[0]
# #print(jobsearch)
# entryStatus = ""
# route = searchedJob.mfdata["ISLEDI"]["Tables"]["job-hdr"]["clearance-route"] if searchedJob.mfdata["ISLEDI"]["Tables"]["job-hdr"]["clearance-route"] else ""
# documentArray = searchedJob.mfdata['ISLEDI']['Tables'].get("job-inst")
# documentsArray = []
# if documentArray:
#     for document in documentArray:
#         docItemCode = document["doc-code"]
#         docItemUser = docItem["sysuser"]
#         if customsDocCodes[docItemCode]:
#             documentData = {
#                 docCode: docItemCode,
#                 docDescription: customsDocCodes[docItemCode],
#             }
#             documentData.append(documentArray)
# # print(documentArray)  

# response = {
# "portalID": portalId,
# "entryStatus": entryStatus,
# "route": route,
# "documentsArray": documentArray
# }
# print(response)


# jobsQuery = session.query(jobs).limit(500).all()
# for jobs in jobsQuery:
#     print(jobs.mfdata['ISLEDI']['Tables']["job-hdr"]["job-disp"])

# print(movies)
# print(movies[0].mfdata['ISLEDI']['Tables']["job-hdr"]["job-disp"]) 
# ['ISLEDI']['Tables']["job-hdr"]["job-disp"]

# print('### Recent jobs list:')
# for jobitem in jobsQuery:
#     print(jobitem)
# print('')      