"""
	This is a small utility script that contains a simple logger
	and a few helper functions.
	
	These are collected here to decrease the clutter in main.py
	(apparantly in vain...)
"""

import sys
import io
import time



class Logger:
	"""
		Simple Logger class that can display progress on the commandline.
		
		
		Authors:
			linvogel
	"""
	
	def __init__(self):
		self.__logger_progress: int = 0
		self.__logger_width: int = 80
		self.__logger_state: str = ""

	def __interrupt(self):
		if self.__logger_progress == 1:
			# flush the out stream first
			print("\nInterrupted!", file=sys.stdout)
		elif self.__logger_progress == 2:
			# flush the error stream first
			print("\nInterrupted!", file=sys.stderr)

	def __print(self, msg: str, file: io.TextIOWrapper):
		if self.__logger_progress != 0:
			self.__interrupt()
		print(msg, file=file, flush=True)

	def setWidth(self, width: int):
		self.__logger_width = width

	def info(self, msg: str):
		self.__print(msg, file=sys.stdout)

	def error(self, msg: str):
		self.__print(msg, file=sys.stderr)

	def info_begin(self, msg: str):
		if self.__logger_progress != 0:
			self.__interrupt()
		self.__logger_state = msg
		self.__logger_progress = 1
		print(msg, end="", flush=True, file=sys.stdout)

	def info_update(self, msg: str):
		if self.__logger_progress == 0:
			return
		blanks: int = self.__logger_width - len(self.__logger_state) - len(msg)
		padding: str = "".join( [ " " ] * blanks)
		line = "\r" + self.__logger_state + padding + msg
		print(line, end="", flush=True, file=sys.stdout)

	def info_end(self, msg: str):
		if self.__logger_progress == 0:
			return
		blanks: int = self.__logger_width - len(self.__logger_state) - len(msg)
		padding: str = "".join( [ " " ] * blanks)
		line = "\r" + self.__logger_state + padding + msg
		print(line, end="\n", flush=True, file=sys.stdout)
		self.__logger_progress = 0
		self.__logger_state = ""

	def error_begin(self, msg: str):
		if self.__logger_progress != 0:
			self.__interrupt()
		self.__logger_state = msg
		self.__logger_progress = 2
		print(msg, end="", flush=True, file=sys.stderr)

	def error_update(self, msg: str):
		if __logger_progress == 0:
			return
		blanks: int = self.__logger_width - len(self.__logger_state) - len(msg)
		padding: str = "".join( [ " " ] * blanks)
		line = "\r" + self.__logger_state + padding + msg
		print(line, end="", flush=True, file=sys.stderr)

	def error_end(self, msg: str):
		if self.__logger_progress == 0:
			return
		blanks: int = self.__logger_width - len(self.__logger_state) - len(msg)
		padding: str = "".join( [ " " ] * blanks)
		line = "\r" + self.__logger_state + padding + msg
		print(line, end="\n", flush=True, file=sys.stderr)
		self.__logger_progress = 0
		self.__logger_state = ""


class Timer:
	"""
		Simple Timer class that can automatically create formatted time strings from when it started to when the string was created, or the timer was stopped
		
		Authors:
			linvogel
	"""
	
	def __init__(self):
		"""
			Create new timer object and start the timer.
			
			Authors:
				linvogel
		"""
		self.start: float = time.time()
		self.stop: float = -1
	
	def stop(self):
		"""
			Stops the timer. If this method is called, any future string representation will read as if it were converted now.
			
			Authors:
				linvogel
		"""
		self.stop: float = time.time()
	
	def __str__(self):
		"""
			Returns string containing the formatted duration recorded by this Timer.
			If the Timer was not stopped, the time current time will be selected as the end time,
			else the time when it was stopped. (duh...)
			
			Authors:
				linvogel
		"""
		duration = (time.time() - self.start) if self.stop < 0 else (self.stop - self.start)
		return time_format(duration)



def time_format(duration: float) -> str:
	"""
		Small helper function to pretty print a duration that may be longer than a minute
		
		Parameters:
			duration:
				The time duration in seconds, including fractional part
		
		Returns:
			A string representation of the input duration
		
		Authors:
			linvogel
	"""
	hours, rem = int(duration / 3600), duration % 3600
	mins, secs = int(rem / 60), rem % 60
	hours_str = str(hours) if hours > 9 else ("0" + str(hours))
	mins_str = str(mins) if mins > 9 else ("0" + str(mins))
	secs_str = ("{:.2f}" if secs >= 10 else "0{:.2f}").format(secs)
	return "{:s}:{:s}:{:s}s".format(hours_str, mins_str, secs_str)
