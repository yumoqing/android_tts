import time
from unitts.basedriver import BaseDriver
from unitts.voice import Voice
from jnius import autoclass
import android

def buildDriver(proxy):
	'''
	Builds a new instance of a driver and returns it for use by the driver
	proxy.

	@param proxy: Proxy creating the driver
	@type proxy: L{driver.DriverProxy}
	'''
	return AndroidNativeTTS(proxy)

Locale = autoclass('java.util.Locale')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
UtteranceProgressListener = autoclass('android.speech.tts.UtteranceProgressListener')

"""
class MyUtteranceProgressListener(UtteranceProgressListener):
	def __init__(self, tts):
		self.tts = tts

	def onStart(self, utteranceId):
		self.tts._proxy.notify('started-utterance')

	def onRangeStart(self, utteranceId, start, end, frame):
		self.tts._proxy.notify('started-word',
					position=start, length=end - start)

	def onError(self, utteranceId, errCode):
		self.tts._proxy.notify('error', Exception(f'errCode={errCode}'))

	def onDone(self, utteranceId):
		self.tts._proxy.notify('finished-uttterance', completed=flag)
"""

def language_by_lang(lang):
    locales = {
        'zh':'zh_CN',
        'en':'en_US',
        'tr':'tr_TR',
        'th':'th_TH',
        'sv':'sv_SE',
        'es':'es_ES',
        'sk':'sk_SK',
        'ru':'ru_RU',
        'ro':'ro_RO',
        'pt':'pt_PT',
        'pl':'pl_PL',
        'no':'no_NO',
        'ko':'ko_KO',
        'ja':'ja_JP',
        'it':'it_IT',
        'id':'id_ID',
        'hu':'hu_HU',
        'hi':'hi_IN',
        'el':'el_GR',
        'de':'de_DE',
        'fr':'fr-FR',
        'nl':'nl-NL',
        'da':'da-DK',
        'cs':'cs-CZ',
        'ar':'ar-SA'
    }
    return locales.get(lang, None)

class AndroidNativeTTS(BaseDriver):
	'''
	Android Navtive speech engine implementation. 
	Documents the interface, notifications,
	properties, and sequencing responsibilities of a driver implementation.

	@ivar _proxy: Driver proxy that manages this instance
	'''
	def __init__(self, proxy):
		'''
		Constructs the driver.

		@param proxy: Proxy creating the driver
		@type proxy: L{driver.DriverProxy}
		'''
		
		super().__init__(proxy)
		self._tts = TextToSpeech(PythonActivity.mActivity, None)
		# listener = MyUtteranceProgressListener(self)
		# self._tts.setOnUtteranceProgressListener(listener)
		self.setProperty('rate', 200)

	def set_voice(self, lang):
		locale = Locale(language_by_lang(lang))
		self._tts.setLanguage(locale)

	def init_listener(self, status):
		print('status=', status)

	def destroy(self):
		'''
		Optional method that will be called when the driver proxy is being
		destroyed. Can cleanup any resources to make sure the engine terminates
		properly.
		'''
		del self._tts
		self._tts = None

	def pre_command(self, sentence):
		return sentence.start_pos, sentence

	def command(self, pos, sentence):
		print('command(). sentence.text
		self.speak_sentence(sentence)

	def speak_sentence(self, sentence):
		self._proxy.setBusy(True)
		self.set_voice(sentence.lang)
		retries = 0
		r = self._tts.speak(text, TextToSpeech.QUEUE_FLUSH, None)
		while retries < 5 and r == -1:
			time.sleep(0.1)
			retries += 1
			r = self._tts.speak(text, TextToSpeech.QUEUE_FLUSH, None)
			
	def getProperty(self, name):
		'''
		Gets a property value of the speech engine. The suppoted properties
		and their values are:

		voices: List of L{voice.Voice} objects supported by the driver
		voice: String ID of the current voice
		rate: Integer speech rate in words per minute
		volume: Floating point volume of speech in the range [0.0, 1.0]

		@param name: Property name
		@type name: str
		@raise KeyError: When the property name is unknown
		'''
		if name == 'voices':
			return self._tts.getVoices()
		if name == 'voice':
			return self._tts.getVoice()
		if name == 'max_text':
			return self._tts.getMaxSpeechInputLength()
		if name == 'rate':
			return self._tts.getSpeechRate()
		return None

	def setProperty(self, name, value):
		if name == 'voices':
			return
		if name == 'voice':
			self._tts.setVoice(value)
			return
		if name == 'rate':
			self._tts.setSpeechRate(value)
		if name == 'volume':
			return
		if name == 'pitch':
			self._tts.setPitch(value)

	def save_to_file(elf, text, filename):
		with open(filename, 'wb') as f:
			self._tts.synthesizeToFile(text, {}, f)
