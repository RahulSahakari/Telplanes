menu_btn = document.querySelector('.hamburger');
mobile_nav = document.querySelector('.mobile-links');

menu_btn.addEventListener('click', function(){

	if(mobile_nav.style.display == "flex"){
		console.log('hi')
		mobile_nav.style.display = "";
	}

	else{
		mobile_nav.style.display = "flex";
	}
	menu_btn.classList.toggle('hamburger-active')
		
})