function colourGetter(uv){
	switch(true)
		{
			case (uv<0):
				colour="cyan";
				break;
				
			case (uv<=3):
				colour="#558B2F";
				break;
			
			case (uv<=6):
				colour="#F9A825";
				break;
					
			case (uv<=8):
				colour="#EF6C00";
				break;
					
			case (uv<11):
				colour="#B71C1C";
				break;
					
			case (uv>=11):
				colour="#6A1B9A";
				break;
			}
			
	return colour;
}
		document.getElementById("UVDisplay").style.backgroundColor=colourGetter(uv);