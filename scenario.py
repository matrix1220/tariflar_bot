
from config import bot

#from photon.client import inline_button
#from photon.utils import format

from photon import OutlineMenu, InlineMenu
from photon.objects import Message
from photon import key, act, explicit_act, back

#from photon.methods import sendMessage

from dbscheme import Company, Tariff, TariffProperty

company_menuset_mode = OutlineMenu

class CompanyTariffMenu(company_menuset_mode):
	keyboard = [
		[ ("Orqaga", back()) ],
	]
	def _init(self, company_id, tariff_id):
		self.company_id = company_id
		self.tariff_id = tariff_id
		super()._init(company_id, tariff_id)

	async def _act(self):
		tariff = self.context.db.query(Tariff).filter_by(
			company_id = self.company_id,
			id = self.tariff_id,
		).first()

		text = f"{tariff.name}\n\n"
		for tariff_property in self.context.db.query(TariffProperty).filter_by(
			company_id = self.company_id,
			tariff_id = self.tariff_id,
		):
			text += f"{tariff_property.name}: {tariff_property.value}\n"

		self.register()
		return Message(text)

class CompanyTariffsMenu(company_menuset_mode):
	def _init(self, company_id):
		self.company_id = company_id
		super()._init(company_id)

	async def _act(self):
		self.keyboard = []
		for tariff in self.context.db.query(Tariff).filter_by(company_id=self.company_id):
			self.keyboard.append([ (tariff.name, act(CompanyTariffMenu, self.company_id, tariff.id)) ])

		self.keyboard.append([ ("Orqaga", back()) ])
		self.register()
		return Message("Ro'yxat:")

class CompanyMenu(company_menuset_mode):
	def _init(self, company_id):
		self.company_id = company_id
		super()._init(company_id)

	# keyboard = [
	# 	[ ("Tariflar", act(CompanyTariffsMenu)) ],
	# 	[ ("Orqaga", back()) ],
	# ]
	async def _act(self):
		self.register()
		self.keyboard = [
			[ ("Tariflar", act(CompanyTariffsMenu, self.company_id)) ],
			[ ("Orqaga", back()) ],
		]
		return Message('Companya menyusi')

class CompaniesMenu(company_menuset_mode):
	async def _act(self):
		self.keyboard = []
		for company in self.context.db.query(Company):
			self.keyboard.append([ (company.name, act(CompanyMenu, company.id)) ])

		self.keyboard.append([ ("Orqaga", back()) ])
		self.register()
		return Message("Ro'yxat:")

@bot.set_main_menu
class MainMenu(OutlineMenu):
	keyboard = [
		[ ("Kompanyalar", act(CompaniesMenu)) ],
		#[ ("Test Menu", act(TestMenu)) ],
	]

	async def _act(self, arg=None):
		self.register()
		return Message(f'Bosh Menu')