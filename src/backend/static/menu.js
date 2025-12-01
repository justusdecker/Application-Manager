menuState = false;

function swapVisibility(_class, b) {
    const val =  b ? "visible" : "hidden";
    console.log(_class, val, b)
    document.getElementById(_class).style.visibility = val;
}

function menuClickToHide() {
    swapVisibility("sidebar", 0);
    swapVisibility("menu-open-btn",1);
    console.log('1');
}

function menuClickToSee() {
    swapVisibility("sidebar", 1);
    swapVisibility("menu-open-btn",0);
    console.log('2');
}