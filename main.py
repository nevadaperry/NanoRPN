import functools
import math
import pickle
import sys
import ttkbootstrap as ttk

class CalcState:
	def __init__(self):
		# The calculation stack; starts with a zero
		self.stack = [0.]
		self.editor_mode = True
		self.editor_text = ""
		self.editor_position = "digits"

class CalcUI:
	def __init__(self, save_file=None):
		self.state = None
		self.save_file = save_file
		if self.save_file:
			try:
				with open(self.save_file, "rb") as file:
					self.state = pickle.load(file)
			except FileNotFoundError:
				print("No existing save file found; starting with default state")
		if not self.state:
			self.state = CalcState()
		
		self.build_window()
		self.window.mainloop()
		
	def build_window(self):
		self.window = ttk.Window(themename="pulse")
		self.window.title("NanoRPN")
		self.window.geometry("640x480")
		self.window.minsize(120, 120)
		# Save on close
		self.window.protocol("WM_DELETE_WINDOW", self.save_stack_state)
		
		# Set general background color to grey so the Labels stand out
		# with their white backgrounds
		ttk.Style().configure("TFrame", background="#efefef")
		
		# Build left and right side
		self.build_left_right_frames()
		# These will be Labels showing the most recent part of the stack
		self.stack_labels = [None] * 8
		self.build_label_side()
		self.build_buttons_side()
	
	def save_stack_state(self):
		try:
			if self.save_file:
				with open(self.save_file, "wb") as file:
					pickle.dump(self.state, file)
		finally:
			self.window.destroy()
	
	def build_left_right_frames(self):
		self.left_frame = ttk.Frame(self.window)
		self.right_frame = ttk.Frame(self.window)
		
		# Sticky attribute makes a widget expandable
		self.left_frame.grid(row=0, column=0, sticky="nsew")
		self.right_frame.grid(row=0, column=1, sticky="nsew")
		
		# Make everything expand vertically and horizontally
		self.window.grid_rowconfigure(0, weight=1)
		self.window.grid_columnconfigure(0, weight=1)
		self.window.grid_columnconfigure(1, weight=2)
	
	def build_label_side(self):
		# Content of stack side (left side of window)
		
		# Set up grid in advance
		for i in range(0, len(self.stack_labels)):
			self.left_frame.rowconfigure(i, weight=1)
		self.left_frame.columnconfigure(0, weight=1)
		
		# Set up labels
		for i in range(0, len(self.stack_labels)):
			self.stack_labels[i] = ttk.Label(self.left_frame,
				anchor="center", text="unset")
			self.stack_labels[i].grid(row=i, column=0,
				sticky="nsew", padx=1, pady=1)
		self.update_stack_labels()
	
	def update_stack_labels(self):
		for i in range(0, len(self.stack_labels)):
			# The labels go bottom-to-top in the UI but the
			# stack goes the other way, so we reverse our index
			position_in_stack = (i - len(self.stack_labels)
									+ len(self.state.stack))
			
			# For the first stack element (bottom of UI), display
			# the string being edited instead of the real number
			# if currently in editing mode
			if (position_in_stack == len(self.state.stack) - 1
								and self.state.editor_mode):
				text = self.state.editor_text
				self.stack_labels[i].configure(bootstyle=ttk.SUCCESS)
			else:
				self.stack_labels[i].configure(bootstyle=ttk.DEFAULT)
				# If the stack is tall enough to go up to this
				# label position in the UI, display it
				if 0 <= position_in_stack < len(self.state.stack):
					text = str(self.state.stack[position_in_stack])
				else:
					text = "~"
			self.stack_labels[i].configure(text=text)
	
	def build_buttons_side(self):
		# Content of buttons side (right side of window)
		
		# Fill space with grid in advance
		for i in range(0, 4):
			self.right_frame.columnconfigure(i, weight=1)
		for i in range(0, 6):
			self.right_frame.rowconfigure(i, weight=1)
		
		btn_texts = ["Drop⬇", "ln", "^", "⬅︎Bksp",
				"(-)", "1/", "√", "/",
				"7", "8", "9", "*",
				"4", "5", "6", "-",
				"1", "2", "3", "+",
				"0", ".", "E", "Enter⬆"]
		btn_keys = ["d", "l", "^", "<BackSpace>",
				"n", "r", "s", "/",
				"7", "8", "9", "*",
				"4", "5", "6", "-",
				"1", "2", "3", "+",
				"0", ".", "e", "<Return>"]
		
		for i in range(0, len(btn_texts)):
			btn = ttk.Button(self.right_frame,
							text=btn_texts[i],
							bootstyle=ttk.SECONDARY,
							command=functools.partial(
							self.handle_btn, btn_texts[i]))
			
			# Bind the button to the applicable keyboard key
			self.window.bind(btn_keys[i],
						functools.partial(self.handle_bind, btn_texts[i]))
			
			# Lay out the buttons into rows and columns by
			# using integer division and modulo
			btn.grid(row=i//4, column=i%4, sticky="nsew",
								padx=1, pady=1)
	
	# In editor mode logic: Reset editor_ vars when entering editor mode;
	# don't bother resetting when leaving editor mode
	def enter_editor_mode_if_needed(self):
		if not self.state.editor_mode:
			self.push_and_enter_editor_mode()
	
	def push_and_enter_editor_mode(self):
		self.state.stack.append(0.0)
		self.state.editor_mode = True
		self.state.editor_text = ""
		self.state.editor_position = "digits"
	
	def editor_number_is_valid(self):
		if not self.state.editor_mode:
			raise ValueError()
		return "" != self.state.editor_text != "-"
	
	def render_editor_number_if_needed(self):
		if self.state.editor_mode and self.editor_number_is_valid():
			self.state.stack[-1] = float(self.state.editor_text)
			self.state.editor_mode = False
	
	def handle_bind(self, btn, event):
		self.handle_btn(btn)
	
	def handle_btn(self, btn):
		# Push/pop/backspace keys
		if btn == "Drop⬇":
			# Shift everything (visually) by popping last element
			if len(self.state.stack) > 0:
				self.state.stack.pop()
			self.state.editor_mode = False
		elif btn == "Enter⬆":
			# Push current number and start editing new number
			if self.state.editor_mode:
				if self.editor_number_is_valid():
					self.render_editor_number_if_needed()
					self.push_and_enter_editor_mode()
			else:
				# Duplicate current number
				#self.state.stack.append(self.state.stack[-1])
				pass
				# Disabled because this probably isn't
				# what the user really wanted to do
		elif btn == "⬅︎Bksp":
			if self.state.editor_mode and self.state.editor_text != "":
				self.state.editor_text = self.state.editor_text[:-1]
		# Number entry keys
		elif btn.isdecimal():
			# [0-9]
			self.enter_editor_mode_if_needed()
			self.state.editor_text += btn
		elif btn == ".":
			self.enter_editor_mode_if_needed()
			if "after_dot" != self.state.editor_position != "after_E":
				self.state.editor_text += "."
				self.state.editor_position = "after_dot"
		elif btn == "E":
			self.enter_editor_mode_if_needed()
			if self.state.editor_position != "after_E":
				if (self.state.editor_text == ""
									or self.state.editor_text == "-"):
					self.state.editor_text += "1"
				self.state.editor_text += "E"
				self.state.editor_position = "after_E"
		# Operations on current number
		elif btn == "(-)":
			if self.state.editor_mode:
				# Manually toggle the first character if it's "-"
				if (len(self.state.editor_text) > 0
									and self.state.editor_text[0] == "-"):
					self.state.editor_text = self.state.editor_text[1:]
				else:
					self.state.editor_text = "-" + self.state.editor_text
			elif len(self.state.stack) >= 1:
				# Negate the float
				self.state.stack[-1] *= -1
		elif btn == "1/":
			if len(self.state.stack) >= 1:
				self.render_editor_number_if_needed()
				self.state.stack[-1] = 1.0 / self.state.stack[-1]
		elif btn == "ln":
			if len(self.state.stack) >= 1:
				self.render_editor_number_if_needed()
				self.state.stack[-1] = math.log(self.state.stack[-1])
		elif btn == "√":
			if len(self.state.stack) >= 1:
				self.render_editor_number_if_needed()
				self.state.stack[-1] = math.sqrt(self.state.stack[-1])
		# Operations on two numbers
		elif btn == "^":
			if len(self.state.stack) >= 2:
				self.render_editor_number_if_needed()
				self.state.stack[-2] **= self.state.stack[-1]
				self.state.stack.pop()
		elif btn == "/":
			if len(self.state.stack) >= 2:
				self.render_editor_number_if_needed()
				self.state.stack[-2] /= self.state.stack[-1]
				self.state.stack.pop()
		elif btn == "*":
			if len(self.state.stack) >= 2:
				self.render_editor_number_if_needed()
				self.state.stack[-2] *= self.state.stack[-1]
				self.state.stack.pop()
		elif btn == "-":
			if len(self.state.stack) >= 2:
				self.render_editor_number_if_needed()
				self.state.stack[-2] -= self.state.stack[-1]
				self.state.stack.pop()
		elif btn == "+":
			if len(self.state.stack) >= 2:
				self.render_editor_number_if_needed()
				self.state.stack[-2] += self.state.stack[-1]
				self.state.stack.pop()
		else:
			raise ValueError()
		self.update_stack_labels()

# User supplied command line arguments begin at argv[1]
if len(sys.argv) == 1:
	CalcUI()
elif len(sys.argv) == 2:
	CalcUI(save_file=sys.argv[1])
else:
	print("error: Expected zero or one argument", file=sys.stderr)
	print("usage: python3 " + sys.argv[0] + " [save-file-path]", file=sys.stderr)
	raise ValueError