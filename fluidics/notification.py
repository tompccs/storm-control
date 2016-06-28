#!/usr/bin/env python

"""
@package notification.py

A class implementing notifications which can be built into protocol .xml files using the following syntax:
	``
	<notify>
		<email to="Thomas.Robbins@cruk.cam.ac.uk" subject="It's time to change the fluids!">
			Dear Tom,

			The first part of the MERFISH protocol is complete. You need to start the second part
			manually and ensure that the fluids are changed in time.
			
			Kind regards,

			MERFISH
		</email>
		<popup>
			The first part of the MERFISH protocol is complete. You need to start the second part
			manually and ensure that the fluids are changed in time.
		</popup>
	</notify>
	``
"""


import smtplib
from email.mime.text import MIMEText
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QCoreApplication

class NotifyParseError(Exception):
	pass

def send_email(recipient, subject, content):
	message = MIMEText(content)
	sender = """"MERFISH Bot" <merfish@cruk.cam.ac.uk>"""
	message['From'] = sender
	message['To'] = recipient
	message['Subject'] = subject

	server = smtplib.SMTP('localhost')
	server.sendmail(sender, recipient.split(","), msg.as_string())
	server.quit()

def make_popup(message):
	# If a Qt application instance exists, display a popup. Otherwise just output to stdout
	if QCoreApplication.instance() != None:
		msg = QMessageBox()
		msg.setText(message)
		msg.exec_()
	else:
		raw_input(message)


class NotifyAction():
	def __init__(self, xml_node):
		if xml_node.tag in ("email", "popup"):
			self.vector = xml_node.tag
		else:
			raise NotifyParseError("Tag not supported")

		self.content = xml_node.text
		if self.vector == "email":
			try:
				self.recipient = xml_node.get("to")
				self.subject = xml_node.get("subject")
			except AttributeError:
				raise NotifyParseError("Missing recipient and/or subject for email")

	def execute(self):
		if self.vector == "email":
			send_email(self.recipient, self.subject, self.content)
		elif self.vector == "popup":
			make_popup(self.content)

class Notification():
	def __init__(self, xml_node):
		self.actions = []
		for action_node in xml_node:
			self.actions.append(NotifyAction(xml_node))

	def execute(self):
		# We need to run the non-blocking notification(s) first
		for action in self.actions:
			if action.vector == "email":
				action.run()
		for action in self.actions:
			if action.vector == "popup":
				action.execute()
