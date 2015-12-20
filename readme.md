# MarkdownView

MarkdownView is a Pythonista UI library component. It is a drop-in replacement for ui.TextView that supports both editing markdown tagged text and viewing it as HTML.

Test link: [LINK](http://iki.fi)

##Contents

1. [Features](#Features)
1. [Link handling](#Link%20handling)
1. [Additional keys](#Additional%20keys)
1. [Design principles/motivation](#Design%20principles/motivation)
1. [API](#API)

## Features <a name='Features'></a> 

* Integrated markdown editing and HTML viewing modes - end editing and HTML is shown, click somewhere on the HTML text and markdown editing starts in the same position.
*  Markdown editing supported by additional keys. (Thanks JonB for help on setting up auxiliary keys.)
* Navigation support when viewing HTML (back, forward).
* Implements ui.TextView API.

## Link handling <a name='Link%20handling'></a>

## Additional keys <a name='Additional%20keys'></a>

* Ggh

## Design principles/motivation <a name='Design%20principles/motivation'></a>

* Provide some rich-text editing capabilities for Pythonista UI scripts
* In a format that is not locked to specific propietary format & program
* Easy to deploy to an existing solution
* Is robust (unlike straight HTML that tends to get confusing with styles etc.)
* Make markdown editing as easy as possible, with the transition between editing and viewing as seamless as possible (in other words, no 'Edit' button)
* But do not require deploying/taking screen space for UI elements like toolbars (i.e. be conscious of and support small screens like iPhone)
* Is lightweight, understandable and manageable by a Python programmer (not the case with using e.g. TinyMCE in a WebView)

## API <a name='API'></a>

### Delegates

### MarkdownView attributes

### Proxied attributes from TextView and WebView

* alignment - as TextView, affects WebView as well
* autocapitalization_type
* autocorrection_type
* auto_content_inset
* 
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
		
* text
* text_color