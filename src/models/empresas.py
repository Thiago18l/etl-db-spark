from sqlalchemy import Column, String, UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Empresa(Base):
    __tablename__ = 'empresas'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    taxpayerRegistry = Column(String, unique=True, nullable=True)
    cnpjOrder = Column(String, nullable=True)
    cnpjDv = Column(String, nullable=True)
    branchIdentifier = Column(String, nullable=True)
    fantasyName = Column(String, nullable=True)
    cadastralSituation = Column(String, nullable=True)
    dateCadastralSituation = Column(String, nullable=True)
    reasonCadastralSituation = Column(String, nullable=True)
    outsideCityName = Column(String, nullable=True)
    country = Column(String, nullable=True)
    startDateActivity = Column(String, nullable=True)
    principalCNAEFiscal = Column(String, nullable=True)
    secondaryCNAEFiscal = Column(String, nullable=True)
    typeOfStreet = Column(String, nullable=True)
    street = Column(String, nullable=True)
    number = Column(String, nullable=True)
    complement = Column(String, nullable=True)
    neighborhood = Column(String, nullable=True)
    cep = Column(String, nullable=True)
    UF = Column(String, nullable=True)
    city = Column(String, nullable=True)
    ddd1 = Column(String, nullable=True)
    phone1 = Column(String, nullable=True)
    ddd2 = Column(String, nullable=True)
    phone2 = Column(String, nullable=True)
    faxDDD = Column(String, nullable=True)
    fax = Column(String, nullable=True)
    email = Column(String, nullable=True)
    specialSituation = Column(String, nullable=True)
    dateSpecialSituation = Column(String, nullable=True)

# Empresas Nordeste
class EmpresasMA(Empresa):
    __tablename__ = 'empresas_ma'

class EmpresasPI(Empresa):
    __tablename__ = 'empresas_pi'

class EmpresasCE(Empresa):
    __tablename__ = 'empresas_ce'

class EmpresasRN(Empresa):
    __tablename__ = 'empresas_rn'

class EmpresasPE(Empresa):
    __tablename__ = 'empresas_pe'

class EmpresasPB(Empresa):
    __tablename__ = 'empresas_pb'

class EmpresasSE(Empresa):
    __tablename__ = 'empresas_se'

class EmpresasAL(Empresa):
    __tablename__ = 'empresas_al'

class EmpresasBA(Empresa):
    __tablename__ = 'empresas_ba'

# Empresas Norte
class EmpresasAM(Empresa):
    __tablename__ = 'empresas_am'

class EmpresasRR(Empresa):
    __tablename__ = 'empresas_rr'

class EmpresasAP(Empresa):
    __tablename__ = 'empresas_ap'

class EmpresasPA(Empresa):
    __tablename__ = 'empresas_pa'

class EmpresasTO(Empresa):
    __tablename__ = 'empresas_to'

class EmpresasRO(Empresa):
    __tablename__ = 'empresas_ro'

# Empresas Centro-Oeste
class EmpresasMT(Empresa):
    __tablename__ = 'empresas_mt'

class EmpresasMS(Empresa):
    __tablename__ = 'empresas_ms'

class EmpresasGO(Empresa):
    __tablename__ = 'empresas_go'

# Empresas Sudeste
class EmpresasSP(Empresa):
    __tablename__ = 'empresas_sp'

class EmpresasRJ(Empresa):
    __tablename__ = 'empresas_rj'

class EmpresasES(Empresa):
    __tablename__ = 'empresas_es'

class EmpresasMG(Empresa):
    __tablename__ = 'empresas_mg'

# Empresas Sul
class EmpresasPR(Empresa):
    __tablename__ = 'empresas_pr'

class EmpresasRS(Empresa):
    __tablename__ = 'empresas_rs'

class EmpresasSC(Empresa):
    __tablename__ = 'empresas_sc'
