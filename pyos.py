import os
import curses
import pycfg
from pyarch import load_binary_into_memory
from pyarch import cpu_t

class process_structure:
	def __init__ (self):
		self.regs = [0, 0, 0, 0, 0, 0, 0, 0]
		self.reg_pc = 0
		self.bin_name = ""
		self.bin_size = 0

class os_t:
	def __init__ (self, cpu, memory, terminal):
		self.cpu = cpu
		self.memory = memory
		self.terminal = terminal

		self.terminal.enable_curses()

		self.console_str = ""
		self.terminal.console_print("this is the console, type the commands here\n")

	def printk(self, msg):
		self.terminal.kernel_print("kernel: " + msg + "\n")

	def panic (self, msg):
		self.terminal.end()
		self.terminal.dprint("kernel panic: " + msg)
		self.cpu.cpu_alive = False
		#cpu.cpu_alive = False

	def interrupt_keyboard (self):
		key = self.terminal.get_key_buffer()

		if ((key >= ord('a')) and (key <= ord('z'))) or ((key >= ord('A')) and (key <= ord('Z'))) or ((key >= ord('0')) and (key <= ord('9'))) or (key == ord(' ')) or (key == ord('-')) or (key == ord('_')) or (key == ord('.')):
			strchar = chr(key)
		elif key == curses.KEY_BACKSPACE:
			return
		elif (key == curses.KEY_ENTER) or (key == ord('\n')):
			return

	def handle_interrupt (self, interrupt):
		return

	def syscall (self):
		#self.terminal.app_print(msg)
		return

	def interrupt_timer (self):
		self.printk("Timer interrupt not implemented yet")

	def handle_interrupt (self, interrupt):
		if interrupt == pycfg.INTERRUPT_MEMORY_PROTECTION_FAULT:
			self.handle_gpf("invalid memory address")
		elif interrupt == pycfg.INTERRUPT_KEYBOARD:
			self.interrupt_keyboard()
		elif interrupt == pycfg.INTERRUPT_TIMER:
			self.interrupt_timer()
		else:
			self.panic("invalid interrupt " + str(interrupt))

	def interrupt_keyboard (self):
		key = self.terminal.get_key_buffer()

		if ((key >= ord('a')) and (key <= ord('z'))) or ((key >= ord('A')) and (key <= ord('Z'))) or ((key >= ord('0')) and (key <= ord('9'))) or (key == ord(' ')) or (key == ord('-')) or (key == ord('_')) or (key == ord('.')):
			self.console_str = self.console_str + chr(key)
			self.terminal.console_print("\r" + self.console_str)
		elif key == curses.KEY_BACKSPACE:
			self.console_str = self.console_str[:-1]
			self.terminal.console_print("\r" + self.console_str)
		elif (key == curses.KEY_ENTER) or (key == ord('\n')):
			self.interpret_cmd(self.console_str)
			self.console_str = ""

	def interpret_cmd (self, cmd):
		if cmd == "bye":
			self.cpu.cpu_alive = False
		elif cmd == "tasks":
			self.task_table_print()
		elif cmd[:3] == "run":
			self.terminal.console_print("\rhere will be load a process")
		else:
			self.terminal.console_print("\rinvalid cmd " + cmd + "\n")