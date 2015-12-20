#coding: utf-8
import ui
from objc_util import *
from markdown2 import markdown
from urllib import quote, unquote
import clipboard
import webbrowser
from string import Template
#from RootView import RootView

class MarkdownView(ui.View):
	
	htmlIntro = Template('''
		<html>
		<head>
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
		<title>Markdown</title>
		<style>
* {
	font-size: $font_size;
	font-family: $font_family;
	-webkit-text-size-adjust: none;
	-webkit-tap-highlight-color: transparent;
}
h1 {
	font-size: 14px;
}
h3 {
	font-style: italic;
}
h4 {
	font-weight: normal;
	font-style: italic;
}
body {
	line-height: 1;
	background: $background_color;
}
		</style>
		<script type="text/javascript">
			function debug(msg) {
				var d = document.getElementById("debug");
				d.href="$debug_prefix" + msg;
				d.click();
			}
		
			function activateLinks() {
				content = document.getElementById("content");
				links = content.getElementsByTagName("a");
				for(var i = 0; i < links.length; i++) {
					links[i].addEventListener('click', anchor_click);
				}
			}
			
			function anchor_click() {
				var e = window.event;
				e.stopPropagation();
				return false;
			}
			
			function text_position() {
				var e = window.event;
				var c = document.getElementById("content");
				var r = document.getElementById("relay");
				var range = new Range();
				range.selectNodeContents(c);
				var rangeEnd = document.caretRangeFromPoint(e.clientX, e.clientY);
				range.setEnd(rangeEnd.startContainer, rangeEnd.startOffset);
				r.href="$link_prefix"+encodeURIComponent(range.toString());
				r.click();
			}
			function initialize() {
				var pos = document.body.clientHeight * $scroll_pos_relative;
				window.scrollTo(0, pos);
				activateLinks();
				var r = document.getElementById("relay");
				r.href = "$init_postfix"
				r.click()
			}
		</script>
		</head>
		<body onload="initialize()">
		<a id="relay" style="display:none"></a>
		<a id="debug" style="display:none"></a>
		<div id="content" onclick="text_position()">
	''')
	htmlOutro = '''
		</div>
		</body>
		</html>
	'''
	
	def __init__(self, background_color = 'white'):
		self.proxy_delegate = None
		self.content_inset = (10,10,10,10)
		self.enable_links = True
		self.background_color = background_color
		
		self.link_prefix = 'pythonista-markdownview:relay?content='
		self.debug_prefix = 'pythonista-markdownview:debug?content='
		self.init_postfix = '#pythonista-markdownview-initialize'
		self.in_doc_prefix = ''
		
		self.to_add_to_beginning = ('', -1)
		# self.custom_keys = custom_key_provider
		self.background_color_name = background_color
		self.markup = ui.TextView(flex='WH')
		#self.markup.background_color = 'lightgrey'
		self.add_subview(self.markup)
		self.web = ui.WebView(flex='WH')
		self.web.scales_page_to_fit = False 
		self.web.content_mode = ui.CONTENT_TOP_LEFT
		self.add_subview(self.web)
		
		self.web.delegate = self
		self.markup.delegate = self
		
		self.markup.text = ''
		self.update_html()
		self.markup.background_color = self.background_color
		self.web.background_color = self.background_color
		self.markup.bounces = False 
		
		self.create_accessory_toolbar()
		
	'''VIEW PROXY PROPERTIES'''
	
		
	'''VIEW PROXY METHODS'''
	
	def size_to_fit(self):
		self.markup.size_to_fit()
		
	'''TEXTVIEW PROXY PROPERTIES'''
		
	@property
	def alignment(self):
		return self.markup.alignment
	@alignment.setter
	def alignment(self, value):
		self.markup.alignment = value
		self.update_html()
		
	@property
	def autocapitalization_type(self):
		return self.markup.autocapitalization_type
	@autocapitalization_type.setter
	def autocapitalization_type(self, value):
		self.markup.autocapitalization_type = value
		
	@property
	def autocorrection_type(self):
		return self.markup.autocorrection_type
	@autocorrection_type.setter
	def autocorrection_type(self, value):
		self.markup.autocorrection_type = value
		
	@property
	def auto_content_inset(self):
		return self.markup.auto_content_inset
	@auto_content_inset.setter
	def auto_content_inset(self, value):
		self.markup.auto_content_inset = value
		
	@property
	def delegate(self):
		return self.proxy_delegate
	@delegate.setter
	def delegate(self, value):
		self.proxy_delegate = value
		
	@property
	def editable(self):
		return self.markup.editable
	@editable.setter
	def editable(self, value):
		self.markup.editable = value
		
	@property
	def font(self):
		return self.markup.font
	@font.setter
	def font(self, value):
		self.markup.font = value
		self.update_html()
		
	@property
	def keyboard_type(self):
		return self.markup.keyboard_type
	@keyboard_type.setter
	def keyboard_type(self, value):
		self.markup.keyboard_type = value
		
	@property
	def selectable(self):
		return self.markup.selectable
	@selectable.setter
	def selectable(self, value):
		self.markup.selectable = value
		
	@property
	def selected_range(self):
		return self.markup.selected_range
	@selected_range.setter
	def selected_range(self, value):
		self.markup.selected_range = value
		
	@property
	def spellchecking_type(self):
		return self.markup.spellchecking_type
	@spellchecking_type.setter
	def spellchecking_type(self, value):
		self.markup.spellchecking_type = value
		
	@property
	def text(self):
		return self.markup.text
	@text.setter
	def text(self, value):
		self.markup.text = value
		self.update_html()
		
	@property
	def text_color(self):
		return self.markup.text_color
	@text_color.setter
	def text_color(self, value):
		self.markup.text_color = value
		self.update_html()
		
	'''TEXTVIEW PROXY METHODS'''
		
	def replace_range(self, range, text):
		self.markup.replace_range(range, text)
		self.update_html()
		
	'''WEBVIEW PROXY PROPERTIES'''
	
	@property
	def scales_page_to_fit(self):
		return self.web.scales_page_to_fit
	@scales_page_to_fit.setter
	def scales_page_to_fit(self, value):
		self.web.scales_page_to_fit = value
		
	'''ACCESSORY TOOLBAR'''
	
	def create_accessory_toolbar(self):
		vobj = ObjCInstance(self.markup)

		keyboardToolbar = ObjCClass('UIToolbar').alloc().init()
		
		keyboardToolbar.sizeToFit()
		
		button_width = 25
		black = ObjCClass('UIColor').alloc().initWithWhite_alpha_(0.0, 1.0)
		
		# Create the buttons
		# Need to retain references to the buttons used
		# to handle clicks
		(self.indentButton, indentBarButton) = self.create_button(u'\u21E5', self.indent)
		
		(self.outdentButton, outdentBarButton) = self.create_button(u'\u21E4', self.outdent)
		
		(self.quoteButton, quoteBarButton) = self.create_button('>', self.block_quote)
		
		(self.linkButton, linkBarButton) = self.create_button('[]', self.link)
		
		(self.anchorButton, anchorBarButton) = self.create_button('<>', self.anchor)
		
		(self.hashButton, hashBarButton) = self.create_button('#', self.heading)
		
		(self.numberedButton, numberedBarButton) = self.create_button('1.', self.numbered_list)
		
		(self.listButton, listBarButton) = self.create_button('•', self.unordered_list)
		
		(self.underscoreButton, underscoreBarButton) = self.create_button('_', self.insert_underscore)
		
		# Flex between buttons
		f = ObjCClass('UIBarButtonItem').alloc().initWithBarButtonSystemItem_target_action_(5, None, None)
		
		doneBarButton = ObjCClass('UIBarButtonItem').alloc().initWithBarButtonSystemItem_target_action_(0, vobj, sel('endEditing:')) 
		
		keyboardToolbar.items = [indentBarButton, f, outdentBarButton, f, quoteBarButton, f, linkBarButton, f, anchorBarButton, f, hashBarButton, f, numberedBarButton, f, listBarButton, f, underscoreBarButton, f, doneBarButton]
		vobj.inputAccessoryView = keyboardToolbar
	
	def create_button(self, label, func):
		button_width = 25
		black = ObjCClass('UIColor').alloc().initWithWhite_alpha_(0.0, 1.0)
		
		action_button = ui.Button()
		action_button.action = func
		accessory_button = ObjCClass('UIBarButtonItem').alloc().initWithTitle_style_target_action_(label, 0, action_button, sel('invokeAction:'))
		accessory_button.width = button_width
		accessory_button.tintColor = black
		return (action_button, accessory_button)
	
	def indent(self, sender):
		def func(line):
			return '  ' + line
		self.transform_lines(func)
		
	def outdent(self, sender):
		def func(line):
			if str(line).startswith('  '):
				return line[2:]
		self.transform_lines(func, ignore_spaces = False)
	
	def insert_star(self, sender):
		self.insert_char('*')
		
	def insert_underscore(self, sender):
		self.insert_char('_')
	
	def insert_char(self, to_insert):
		textview = self.markup
		(start, end) = textview.selected_range
		if start <> end:
			to_insert = to_insert + textview.text[start:end] + to_insert
		textview.replace_range((start, end), to_insert)
		if start <> end:
			textview.selected_range = (start, end + 2)
		
	def heading(self, sender):
		def func(line):
			if str(line).startswith('###'):
				return line[3:]
			else:
				return '#' + line
		self.transform_lines(func)
		
	def numbered_list(self, data):
		def func(line):
			if line.startswith('1. '):
				return line[3:]
			elif line.startswith('* '):
				return '1. ' + line[2:]
			else:
				return '1. ' + line
		self.transform_lines(func)
		
	def unordered_list(self, sender):
		def func(line):
			if str(line).startswith('* '):
				return line[2:]
			elif line.startswith('1. '):
				return '* ' + line[3:]
			else:
				return '* ' + line
		self.transform_lines(func)
		
	def block_quote(self, sender):
		def func(line):
			return '> ' + line
		self.transform_lines(func, ignore_spaces = False)
		
	def link(self, sender):
		templ = "[#]($)"
		(start, end) = self.markup.selected_range
		templ = templ.replace('$', self.markup.text[start:end])
		new_start = start + templ.find('#')
		new_end = new_start + (end - start)
		templ = templ.replace('#', self.markup.text[start:end])
		self.markup.replace_range((start, end), templ)
		self.markup.selected_range = (new_start, new_end)
		
	def anchor(self, sender):
		templ = " <a name='#'></a>"
		(start, end) = self.markup.selected_range
		link_label = self.markup.text[start:end]
		link_name = quote(self.markup.text[start:end])
		templ = templ.replace('#', link_name)
		self.markup.replace_range((end, end), templ)
		link = "[" + link_label + "](#" + link_name + ")"
		clipboard.set(link)
		
	def make_list(self, list_marker):
		self.get_lines()
		
	def transform_lines(self, func, ignore_spaces = True):
		(orig_start, orig_end) = self.markup.selected_range
		(lines, start, end) = self.get_lines()
		replacement = []
		for line in lines:
			spaces = ''
			if ignore_spaces:
				space_count = len(line) - len(line.lstrip(' '))
				if space_count > 0:
					spaces = line[:space_count]
					line = line[space_count:]
			replacement.append(spaces + func(line))
		self.markup.replace_range((start, end), '\n'.join(replacement))
		new_start = orig_start + len(replacement[0]) - len(lines[0])
		if new_start < start:
			new_start = start
		end_displacement = 0
		for index, line in enumerate(lines):
			end_displacement += len(replacement[index]) - len(line)
		new_end = orig_end + end_displacement
		if new_end < new_start:
			new_end = new_start
		self.markup.selected_range = (new_start, new_end)
		
	def get_lines(self):
		(start, end) = self.markup.selected_range
		text = self.markup.text
		new_start = text.rfind('\n', 0, start)
		if new_start == -1: new_start = 0
		else: new_start += 1
		new_end = text.find('\n', end)
		if new_end == -1: new_end = len(text)
		#else: new_end -= 1
		if new_end < new_start: new_end = new_start
		return (text[new_start:new_end].split('\n'), new_start, new_end)
	
	'''def layout(self):
		(top, left, bottom, right) = self.content_inset
		self.markup.frame = (left, top, self.width - left - right, self.height - top - bottom)
		self.web.frame = self.markup.frame'''
		#self.over.frame = self.web.frame
		
	def toHtml(self, scroll_pos_relative = 0):
		return self.htmlIntro.safe_substitute(
			background_color = self.background_color_name, 
			font_family = 'helvetica', #self.markup.font[0],
			font_size = '12px', #str(self.markup.font[1]) + 'px',
			scroll_pos_relative = scroll_pos_relative,
			init_postfix = self.init_postfix,
			link_prefix = self.link_prefix,
			debug_prefix = self.debug_prefix
		) + markdown(self.markup.text) + self.htmlOutro
		
	def update_html(self):
		self.web.load_html(self.toHtml())
		
	def start_editing(self, words):
		self.web.hidden = True
		caret_pos = 0
		marked = self.markup.text
		for word in words:
			caret_pos = marked.find(word, caret_pos) + len(word)
		self.markup.begin_editing()
		self.markup.selected_range = (caret_pos, caret_pos)
		
	#def keyboard_frame_did_change(self, frame):
		#if self.custom_keys:
			#self.custom_keys.change(frame, self.markup)
	
	def can_call(self, func_name):
		if not self.proxy_delegate:
			return False
		return callable(getattr(self.proxy_delegate, func_name, None))
	
	'''TEXTVIEW DELEGATES'''
	def textview_did_end_editing(self, textview):
		(start, end) = self.markup.selected_range
		scroll_pos_relative = self.markup.content_offset / self.markup.content_size[1]
		self.web.load_html(self.toHtml(scroll_pos_relative))
		self.web.hidden = False
		if self.can_call('textview_did_end_editing'):
			self.proxy_delegate.textview_did_end_editing(textview)
			
	def textview_should_change(self, textview, range, replacement):
		should_change = True
		self.to_add_to_beginning = ('', -1)
		if self.can_call('textview_should_change'):
			should_change =  self.proxy_delegate.textview_should_change(textview, range, replacement)
		if should_change == True and replacement == '\n': #and range[0] == range[1] 
			pos = range[0]
			next_line_prefix = ''
			# Get to next line
			pos = self.markup.text.rfind('\n', 0, pos)
			if not pos == -1:
				pos = pos + 1
				rest = self.markup.text[pos:]
				# Copy leading spaces
				space_count = len(rest) - len(rest.lstrip(' '))
				if space_count > 0:
					next_line_prefix += rest[:space_count]
					rest = rest[space_count:]
				# Check for prefixes
				prefixes = [ '1. ', '+ ', '- ', '* ']
				for prefix in prefixes:
					if rest.startswith(prefix):
						next_line_prefix += prefix
						break
				if len(next_line_prefix) > 0:
					diff = range[0] - pos
					if diff < len(next_line_prefix):
						next_line_prefix = next_line_prefix[:diff]
					self.to_add_to_beginning = (next_line_prefix, range[0]+1)		
		return should_change
			
	def textview_did_change(self, textview):
		add = self.to_add_to_beginning
		if add[1] > -1:
			self.to_add_to_beginning = ('', -1)
			self.markup.replace_range((add[1], add[1]), add[0])
		if self.can_call('textview_did_change'):
			self.proxy_delegate.textview_did_change(textview)
			
	def textview_should_begin_editing(self, textview):
		if self.can_call('textview_should_begin_editing'):
			return self.proxy_delegate.textview_should_begin_editing(textview)
		else:
			return True
	def textview_did_begin_editing(self, textview):
		if self.can_call('textview_did_begin_editing'):
			self.proxy_delegate.textview_did_begin_editing(textview)
	
	def textview_did_change_selection(self, textview):
		if self.can_call('textview_did_change_selection'):
			self.proxy_delegate.textview_did_change_selection(textview)
			
	'''WEBVIEW DELEGATES'''
	
	def webview_should_start_load(self, webview, url, nav_type):
		# Click, should start edit in markdown
		if url.startswith(self.link_prefix):
			left_side = unquote(url.replace(self.link_prefix, ''))
			self.start_editing(left_side.split())
			#webview.stop()
			return False
		# Debug message from web page, print to console
		elif url.startswith(self.debug_prefix):
			debug_text = unquote(url.replace(self.debug_prefix, ''))
			print debug_text
			return False
		# Loaded by the web view at start, allow
		elif url.startswith('about:blank'):
			return True
		# Custom WebView initialization message
		# Used to check if in-doc links starting with '#'
		# have extra stuff in front
		elif url.endswith(self.init_postfix):
			self.in_doc_prefix = url[:len(url)-len(self.init_postfix)]
			return False
			
		# If link starts with the extra stuff detected
		# at initialization, remove the extra
		if url.startswith(self.in_doc_prefix):
			url = url[len(self.in_doc_prefix):]
		
		# Check for custom link handling
		if self.can_call('webview_should_start_load'):
			return self.proxy_delegate.webview_should_start_load(webview, url, nav_type)
		# Handle in-doc links within the page
		elif url.startswith('#'):
			return True
		# Open 'http(s)' links in Safari
		# 'file' in built-in browser
		# Others like 'twitter' as OS decides
		else:
			if url.startswith('http:') or url.startswith('https:'):
				url = 'safari-' + url
			webbrowser.open(url)
			return False
		
	def webview_did_start_load(self, webview):
		if self.can_call('webview_did_start_load'):
			self.proxy_delegate.webview_did_start_load(webview)
	def webview_did_finish_load(webview):
		if self.can_call('webview_did_finish_load'):
			self.proxy_delegate.webview_did_finish_load(webview)
	def webview_did_fail_load(webview, error_code, error_msg):
		if self.can_call('webview_did_fail_load'):
			self.proxy_delegate.webview_did_fail_load(webview, error_code, error_msg)
				
### CUT HERE - everything below this line is for demonstration only

if __name__ == "__main__":
	import os
	class SaveDelegate (object):
		def textview_did_change(self, textview):
			readme = os.path.join(os.path.expanduser('~/Documents'), 'readme.md')
			with open(readme, "w") as file_out:
				file_out.write(textview.text)
	init_string = ''
	readme = os.path.join(os.path.expanduser('~/Documents'), 'readme.md')
	editor = MarkdownView()
	editor.name = 'MarkdownView Documentation'
	if os.path.exists(readme):
		with open(readme) as file_in:
			init_string = file_in.read()
	editor.text = init_string
	editor.delegate = SaveDelegate()
	#editor.content_inset = (20, 20, 20, 20)
	#editor2.background_color = 'grey'
	editor.present(style='fullscreen', hide_title_bar=False) 