
let wheelnumbersAC = [0, 26, 3, 35, 12, 28, 7, 29, 18, 22, 9, 31, 14, 20, 1, 33, 16, 24, 5, 10, 23, 8, 30, 11, 36, 13, 27, 6, 34, 17, 25, 2, 21, 4, 19, 15, 32];

let wheel;
let ballTrack;

function initWheel() {
	setTimeout(function () {
		buildWheel(document.getElementsByClassName("main-container")[0]);
		wheel = document.getElementsByClassName('wheel')[0];
		ballTrack = document.getElementsByClassName('ballTrack')[0];
	}, 1000);
}




/**
 * Random Spin with 
 */
function spin() {
	var winningSpin = Math.floor(Math.random() * 36);
	spinWheel(winningSpin);
}


/**
 * Function to spin the wheel to a specifique number
 * @param {INT} winningSpin a value between 0 and 36 
 */
window.spinWheel = (winningSpin) => {
	for (i = 0; i < wheelnumbersAC.length; i++) {
		if (wheelnumbersAC[i] == winningSpin) {
			var degree = (i * 9.73) + 362;
		}
	}
	wheel.style.cssText = 'animation: wheelRotate 5s linear infinite;';
	ballTrack.style.cssText = 'animation: ballRotate 1s linear infinite;';

	setTimeout(function () {
		ballTrack.style.cssText = 'animation: ballRotate 2s linear infinite;';
		style = document.createElement('style');
		style.type = 'text/css';
		style.innerText = '@keyframes ballStop {from {transform: rotate(0deg);}to{transform: rotate(-' + degree + 'deg);}}';
		document.head.appendChild(style);
	}, 2000);
	setTimeout(function () {
		ballTrack.style.cssText = 'animation: ballStop 3s linear;';
	}, 6000);
	setTimeout(function () {
		ballTrack.style.cssText = 'transform: rotate(-' + degree + 'deg);';
	}, 9000);
	setTimeout(function () {
		wheel.style.cssText = '';
		style.remove();
	}, 10000);
}

/**
 * Create the wheel with HTML components
 * @param {HTMLElement} container | element where the wheel will be create
 */
function buildWheel(mainContainer) {
	let container = document.createElement('div');
	container.setAttribute('id', 'container-roulette');
	mainContainer.append(container);

	let wheel = document.createElement('div');
	wheel.setAttribute('class', 'wheel');

	let outerRim = document.createElement('div');
	outerRim.setAttribute('class', 'outerRim');
	wheel.append(outerRim);

	//order of the number in the wheels
	let numbers = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26];
	for (i = 0; i < numbers.length; i++) {
		let a = i + 1;
		let spanClass = (numbers[i] < 10) ? 'single' : 'double';
		let sect = document.createElement('div');
		sect.setAttribute('id', 'sect' + a);
		sect.setAttribute('class', 'sect');
		let span = document.createElement('span');
		span.setAttribute('class', spanClass);
		span.innerText = numbers[i];
		sect.append(span);
		let block = document.createElement('div');
		block.setAttribute('class', 'block');
		sect.append(block);
		wheel.append(sect);
	}

	let pocketsRim = document.createElement('div');
	pocketsRim.setAttribute('class', 'pocketsRim');
	wheel.append(pocketsRim);

	let ballTrack = document.createElement('div');
	ballTrack.setAttribute('class', 'ballTrack');
	let ball = document.createElement('div');
	ball.setAttribute('class', 'ball');
	ballTrack.append(ball);
	wheel.append(ballTrack);

	let pockets = document.createElement('div');
	pockets.setAttribute('class', 'pockets');
	wheel.append(pockets);

	let cone = document.createElement('div');
	cone.setAttribute('class', 'cone');
	wheel.append(cone);

	let turret = document.createElement('div');
	turret.setAttribute('class', 'turret');
	wheel.append(turret);

	let turretHandle = document.createElement('div');
	turretHandle.setAttribute('class', 'turretHandle');
	let thendOne = document.createElement('div');
	thendOne.setAttribute('class', 'thendOne');
	turretHandle.append(thendOne);
	let thendTwo = document.createElement('div');
	thendTwo.setAttribute('class', 'thendTwo');
	turretHandle.append(thendTwo);
	wheel.append(turretHandle);

	container.append(wheel);
}
