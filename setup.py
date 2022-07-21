try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

#with open('README.rst', 'r') as f:
#	long_description = f.read()

setup(
	name='android_tts',
	packages=['android_tts'],
	version='0.0.1',
	description='a pyttsx3 driver for android device, it use android.speech.tts.',
	long_description='',
	summary='pyttsx3 driver for android device',
	author='Yu Moqing',
	url='https://github.com/yumoqing/android_tts',
	author_email='yumoqing@gmail.com',
	# install_requires=install_requires ,
	keywords=['pyttsx' , 'android', 'offline tts engine'],
	classifiers = [
		  'Intended Audience :: End Users/Desktop',
		  'Intended Audience :: Developers',
		  'Intended Audience :: Information Technology',
		  'Intended Audience :: System Administrators',
		  'Operating System :: android :: android TV',
		  'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
		  'Programming Language :: Python :: 3'
	],
)
