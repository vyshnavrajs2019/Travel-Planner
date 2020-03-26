urls = [
	'https://www.google.com/maps/place/Kasaragod,+Kerala/@12.4156083,75.0601568,10z/data=!4m5!3m4!1s0x3ba482155de6aad1:0x3a07d5464844020a!8m2!3d12.4995966!4d74.9869276',
	'https://www.google.com/maps/place/Kannur,+Kerala/@11.8666858,75.3523103,14z/data=!3m1!4b1!4m5!3m4!1s0x3ba422b9b2aca753:0x380605a11ce24f6c!8m2!3d11.8744775!4d75.3703662',
	'https://www.google.com/maps/place/Kozhikode,+Kerala/@11.2561386,75.6703814,11z/data=!3m1!4b1!4m5!3m4!1s0x3ba65938563d4747:0x32150641ca32ecab!8m2!3d11.2587531!4d75.78041',
	'https://www.google.com/maps/place/Wayanad,+Kerala/@11.7147961,75.8282918,10z/data=!3m1!4b1!4m5!3m4!1s0x3ba60cf91a9c5f0d:0x71dd4da2e1d3e46f!8m2!3d11.6853575!4d76.1319953',
	'https://www.google.com/maps/place/Malappuram,+Kerala/@11.0619439,76.0332862,13z/data=!3m1!4b1!4m5!3m4!1s0x3ba64a9be29b058f:0x23e371e0d4c30d8e!8m2!3d11.0509762!4d76.0710967',
	'https://www.google.com/maps/place/Palakkad,+Kerala/@10.7882494,76.6188017,13z/data=!3m1!4b1!4m5!3m4!1s0x3ba86dfa087d31ad:0xf542d6eb7a870a56!8m2!3d10.7867303!4d76.6547932',
	'https://www.google.com/maps/place/Thrissur,+Kerala/@10.5115487,76.1530376,12z/data=!3m1!4b1!4m5!3m4!1s0x3ba7ee15ed42d1bb:0x82e45aa016ca7db!8m2!3d10.5276416!4d76.2144349',
	'https://www.google.com/maps/place/Ernakulam,+Kerala/@9.9711834,76.1678608,11z/data=!3m1!4b1!4m5!3m4!1s0x3b080d08f976f3a9:0xe9cdb444f06ed454!8m2!3d9.9816358!4d76.2998842',
	'https://www.google.com/maps/place/Idukki+Twp,+Kerala/@9.8564875,76.9118412,13z/data=!3m1!4b1!4m5!3m4!1s0x3b07ba46467e69c3:0xac9b7a0e53bf72d2!8m2!3d9.8583987!4d76.9527836',
	'https://www.google.com/maps/place/Alappuzha,+Kerala/@9.501199,76.271893,12z/data=!3m1!4b1!4m5!3m4!1s0x3b0884f1aa296b61:0xb84764552c41f85a!8m2!3d9.4980667!4d76.3388484',
	'https://www.google.com/maps/place/Pathanamthitta,+Kerala/@9.260413,76.7429559,13z/data=!3m1!4b1!4m5!3m4!1s0x3b06152f4f9705d7:0x4d93dd296d4b4abc!8m2!3d9.2647582!4d76.7870414',
	'https://www.google.com/maps/place/Kollam,+Kerala/@8.9042253,76.5248605,12z/data=!3m1!4b1!4m5!3m4!1s0x3b05fc5bdda9c621:0x8bf03195267372f7!8m2!3d8.8932118!4d76.6141396',
	'https://www.google.com/maps/place/Thiruvananthapuram,+Kerala/@8.5000474,76.783734,11z/data=!3m1!4b1!4m5!3m4!1s0x3b05bbb805bbcd47:0x15439fab5c5c81cb!8m2!3d8.5241391!4d76.9366376'
]

districts = {}
for url in urls:
	a = url.split('https://www.google.com/maps/place/')[1]
	b = a.split('/data=')[0]
	c, d = b.split('/')
	e = c.split(',')[0].lower()
	f, g, h = d.split(',')
	i = f.split('@')[1]
	districts[e] = [float(i), float(g)]

print(districts)
