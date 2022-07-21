# from pyttsx3.voice import Voice
import time
from jnius import autoclass
import android
from android.permissions import request_permissions, Permission
request_permissions([Permission.INTERNET])

"""
		from jnius import autoclass
		Locale = autoclass('java.util.Locale')
		PythonActivity = autoclass('org.renpy.android.PythonActivity')
		TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
		tts = TextToSpeech(PythonActivity.mActivity, None)

		# Play something in english
		tts.setLanguage(Locale.US)
		tts.speak('Hello World.', TextToSpeech.QUEUE_FLUSH, None)

		# Queue something in french
		tts.setLanguage(Locale.FRANCE)
		tts.speak('Bonjour tout le monde.', TextToSpeech.QUEUE_ADD, None)

"""

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

class AndroidNativeTTS(object):
	'''
	Android Navtive speech engine implementation. Documents the interface, notifications,
	properties, and sequencing responsibilities of a driver implementation.

	@ivar _proxy: Driver proxy that manages this instance
	@type _proxy: L{driver.DriverProxy}
	@ivar _config: Dummy configuration
	@type _config: dict
	@ivar _looping: True when in the dummy event loop, False when not
	@ivar _looping: bool
	'''
	def __init__(self, proxy):
		'''
		Constructs the driver.

		@param proxy: Proxy creating the driver
		@type proxy: L{driver.DriverProxy}
		'''

		self._tts = TextToSpeech(PythonActivity.mActivity, None)
		# listener = MyUtteranceProgressListener(self)
		# self._tts.setOnUtteranceProgressListener(listener)
		self.setProperty('rate', 200)
		self._proxy = proxy
		self._looping = False
		self._completed = True

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

	def startLoop(self):
		'''
		Starts a blocking run loop in which driver callbacks are properly
		invoked.

		@precondition: There was no previous successful call to L{startLoop}
			without an intervening call to L{stopLoop}.
		'''
		first = True
		self._looping = True
		while self._looping:
			if first:
				self._proxy.setBusy(False)
				first = False
			time.sleep(0.5)

	def endLoop(self):
		'''
		Stops a previously started run loop.

		@precondition: A previous call to L{startLoop} suceeded and there was
			no intervening call to L{endLoop}.
		'''
		self._looping = False

	def iterate(self):
		'''
		Iterates from within an external run loop.
		'''
		self._proxy.setBusy(False)
		yield

	def say(self, text):
		'''
		Speaks the given text. Generates the following notifications during
		output:

		started-utterance: When speech output has started
		started-word: When a word is about to be spoken. Includes the character
			"location" of the start of the word in the original utterance text
			and the "length" of the word in characters.
		finished-utterance: When speech output has finished. Includes a flag
			indicating if the entire utterance was "completed" or not.

		The proxy automatically adds any "name" associated with the utterance
		to the notifications on behalf of the driver.

		When starting to output an utterance, the driver must inform its proxy
		that it is busy by invoking L{driver.DriverProxy.setBusy} with a flag
		of True. When the utterance completes or is interrupted, the driver
		inform the proxy that it is no longer busy by invoking
		L{driver.DriverProxy.setBusy} with a flag of False.

		@param text: Unicode text to speak
		@type text: unicode
		'''
		self._proxy.setBusy(True)
		self._tts.speak(text, TextToSpeech.QUEUE_ADD, None)

	def stop(self):
		'''
		Stops any current output. If an utterance was being spoken, the driver
		is still responsible for sending the closing finished-utterance
		notification documented above and resetting the busy state of the
		proxy.
		'''
		if self._proxy.isBusy():
			self._completed = False
		self._tts.stop()

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
		'''
		Sets one of the supported property values of the speech engine listed
		above. If a value is invalid, attempts to clip it / coerce so it is
		valid before giving up and firing an exception.

		@param name: Property name
		@type name: str
		@param value: Property value
		@type value: object
		@raise KeyError: When the property name is unknown
		@raise ValueError: When the value cannot be coerced to fit the property
		'''
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
