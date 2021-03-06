from flask import Flask, jsonify, request
from PIL import Image
from random import randint
import numpy
import sys
from helper import *
import base64
from io import BytesIO

app = Flask(__name__)

@app.route("/encrypt",methods=["POST"])
def home():
	data = request.json
	im = Image.open(BytesIO(base64.b64decode(data['img'])))
	pix = im.load()
	#Obtaining the RGB matrices
	r = []
	g = []
	b = []
	for i in range(im.size[0]):
		r.append([])
		g.append([])
		b.append([]) 
		for j in range(im.size[1]):
			rgbPerPixel = pix[i,j]
			r[i].append(rgbPerPixel[0])
			g[i].append(rgbPerPixel[1])
			b[i].append(rgbPerPixel[2])

	m = im.size[0]
	n = im.size[1]

	# Vectors Kr and Kc
	alpha = 8
	Kr = [randint(0,pow(2,alpha)-1) for i in range(m)]
	Kc = [randint(0,pow(2,alpha)-1) for i in range(n)]
	ITER_MAX = 1

	# print('Vector Kr : ', Kr)
	# print('Vector Kc : ', Kc)

	f = open('keys.txt','w+')
	f.write('Vector Kr : \n')
	for a in Kr:
		f.write(str(a) + '\n')
	f.write('Vector Kc : \n')
	for a in Kc:
		f.write(str(a) + '\n')
	f.write('ITER_MAX : \n')
	f.write(str(ITER_MAX) + '\n')


	for iterations in range(ITER_MAX):
		# For each row
		for i in range(m):
			rTotalSum = sum(r[i])
			gTotalSum = sum(g[i])
			bTotalSum = sum(b[i])
			rModulus = rTotalSum % 2
			gModulus = gTotalSum % 2
			bModulus = bTotalSum % 2
			if(rModulus==0):
				r[i] = numpy.roll(r[i],Kr[i])
			else:
				r[i] = numpy.roll(r[i],-Kr[i])
			if(gModulus==0):
				g[i] = numpy.roll(g[i],Kr[i])
			else:
				g[i] = numpy.roll(g[i],-Kr[i])
			if(bModulus==0):
				b[i] = numpy.roll(b[i],Kr[i])
			else:
				b[i] = numpy.roll(b[i],-Kr[i])
		# For each column
		for i in range(n):
			rTotalSum = 0
			gTotalSum = 0
			bTotalSum = 0
			for j in range(m):
				rTotalSum += r[j][i]
				gTotalSum += g[j][i]
				bTotalSum += b[j][i]
			rModulus = rTotalSum % 2
			gModulus = gTotalSum % 2
			bModulus = bTotalSum % 2
			if(rModulus==0):
				upshift(r,i,Kc[i])
			else:
				downshift(r,i,Kc[i])
			if(gModulus==0):
				upshift(g,i,Kc[i])
			else:
				downshift(g,i,Kc[i])
			if(bModulus==0):
				upshift(b,i,Kc[i])
			else:
				downshift(b,i,Kc[i])
		# For each row
		for i in range(m):
			for j in range(n):
				if(i%2==1):
					r[i][j] = r[i][j] ^ Kc[j]
					g[i][j] = g[i][j] ^ Kc[j]
					b[i][j] = b[i][j] ^ Kc[j]
				else:
					r[i][j] = r[i][j] ^ rotate180(Kc[j])
					g[i][j] = g[i][j] ^ rotate180(Kc[j])
					b[i][j] = b[i][j] ^ rotate180(Kc[j])
		# For each column
		for j in range(n):
			for i in range(m):
				if(j%2==0):
					r[i][j] = r[i][j] ^ Kr[i]
					g[i][j] = g[i][j] ^ Kr[i]
					b[i][j] = b[i][j] ^ Kr[i]
				else:
					r[i][j] = r[i][j] ^ rotate180(Kr[i])
					g[i][j] = g[i][j] ^ rotate180(Kr[i])
					b[i][j] = b[i][j] ^ rotate180(Kr[i])


	for i in range(m):
		for j in range(n):
			pix[i,j] = (r[i][j],g[i][j],b[i][j])

	im.save('encrypted_images/example.png')
	
	output_buffer = BytesIO()

	im.save(output_buffer, format="PNG")
	img_str = base64.b64encode(output_buffer.getvalue())
	return {"img":str(img_str,'utf-8'),"kr":Kr,"kc":Kc,"iter_max":ITER_MAX}


@app.route("/decrypt",methods=["POST"])
def home1():
	data = request.json
	im = Image.open(BytesIO(base64.b64decode(data['img'])))
	pix = im.load()
	
	

	#Obtaining the RGB matrices
	r = []
	g = []
	b = []
	for i in range(im.size[0]):
		r.append([])
		g.append([])
		b.append([]) 
		for j in range(im.size[1]):
			rgbPerPixel = pix[i,j]
			r[i].append(rgbPerPixel[0])
			g[i].append(rgbPerPixel[1])
			b[i].append(rgbPerPixel[2])

	m = im.size[0]
	n = im.size[1]

	Kr = data["kr"]
	Kc = data["kc"]
	ITER_MAX = data["iter_max"]
	

	# print('Enter value of Kr')

	# for i in range(m):
	# 	Kr.append(int(input()))

	# print('Enter value of Kc')
	# for i in range(n):
	# 	Kc.append(int(input()))

	# print('Enter value of ITER_MAX')
	# ITER_MAX = int(input())

	# print(Kr)
	for iterations in range(ITER_MAX):
		# For each column
		for j in range(n):
			for i in range(m):
				if(j%2==0):
					r[i][j] = r[i][j] ^ Kr[i]
					g[i][j] = g[i][j] ^ Kr[i]
					b[i][j] = b[i][j] ^ Kr[i]
				else:
					r[i][j] = r[i][j] ^ rotate180(Kr[i])
					g[i][j] = g[i][j] ^ rotate180(Kr[i])
					b[i][j] = b[i][j] ^ rotate180(Kr[i])
		# For each row
		for i in range(m):
			for j in range(n):
				if(i%2==1):
					r[i][j] = r[i][j] ^ Kc[j]
					g[i][j] = g[i][j] ^ Kc[j]
					b[i][j] = b[i][j] ^ Kc[j]
				else:
					r[i][j] = r[i][j] ^ rotate180(Kc[j])
					g[i][j] = g[i][j] ^ rotate180(Kc[j])
					b[i][j] = b[i][j] ^ rotate180(Kc[j])
		# For each column
		for i in range(n):
			rTotalSum = 0
			gTotalSum = 0
			bTotalSum = 0
			for j in range(m):
				rTotalSum += r[j][i]
				gTotalSum += g[j][i]
				bTotalSum += b[j][i]
			rModulus = rTotalSum % 2
			gModulus = gTotalSum % 2
			bModulus = bTotalSum % 2
			if(rModulus==0):
				downshift(r,i,Kc[i])
			else:
				upshift(r,i,Kc[i])
			if(gModulus==0):
				downshift(g,i,Kc[i])
			else:
				upshift(g,i,Kc[i])
			if(bModulus==0):
				downshift(b,i,Kc[i])
			else:
				upshift(b,i,Kc[i])

		# For each row
		for i in range(m):
			rTotalSum = sum(r[i])
			gTotalSum = sum(g[i])
			bTotalSum = sum(b[i])
			rModulus = rTotalSum % 2
			gModulus = gTotalSum % 2
			bModulus = bTotalSum % 2
			if(rModulus==0):
				r[i] = numpy.roll(r[i],-Kr[i])
			else:
				r[i] = numpy.roll(r[i],Kr[i])
			if(gModulus==0):
				g[i] = numpy.roll(g[i],-Kr[i])
			else:
				g[i] = numpy.roll(g[i],Kr[i])
			if(bModulus==0):
				b[i] = numpy.roll(b[i],-Kr[i])
			else:
				b[i] = numpy.roll(b[i],Kr[i])

	for i in range(m):
		for j in range(n):
			pix[i,j] = (r[i][j],g[i][j],b[i][j])

	im.save('decrypted_images/example.png')
	output_buffer = BytesIO()

	im.save(output_buffer, format="PNG")
	img_str = base64.b64encode(output_buffer.getvalue())
	return str(img_str,'utf-8')


if __name__ == '__main__':
	app.run(debug=True)