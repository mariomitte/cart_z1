function docReady(fn) {
  // see if DOM is already available
  if (document.readyState === "complete" || document.readyState === "interactive") {
    // call on next available tick
    setTimeout(fn, 1);
  } else {
    document.addEventListener("DOMContentLoaded", fn);
  }
}

function kodiusWebsite() {
  // HAMBURGER MENU
  // let hamburgerMenu = document.querySelector('.hamburger')
  // let storeMenu = document.querySelector('.store')
  // let hamburgerMenuContent = document.querySelector('.hamburger__content')
  // let storeMenuContent = document.querySelector('.store__content')
  let nav = document.querySelector('.nav')
  let logo = document.querySelector('.nav__logo-image')
  let originalLogo = logo.src
  let originalHeaderColor = nav.classList.contains('nav--dark') ? 'nav--dark' : 'nav--light'

  // Reveal & Close Panels
  var revealMenu = function (classButton, classContent) {
    let buttonReveal = document.querySelector(`.${classButton}`)
    let item = document.querySelectorAll(`.${classContent}`)
    let navigation = document.querySelector('.shop__navigation-links')
    let navMenuHamburger = document.querySelector('.hamburger')
    let navMenuReturn = document.querySelector('.menu__return')
    let storeSecondaryReturn = document.querySelector('.secondary__return')

    item.forEach(function(item) {
      buttonReveal.addEventListener('click', () => {
        // Slide the menu
        if (item.classList.contains(`${classContent}--closed`)) {
          if (classButton === classButton) {
            navMenuReturn.classList.add('menu__return--show')
            navMenuReturn.classList.remove('menu__return--hide')
            // navMenuHamburger.classList.add('hamburger--hide')
            // navMenuHamburger.classList.remove('hamburger--show')
            toggleScroll()
          }
          item.classList.add(`${classContent}--opened`)
          item.classList.remove(`${classContent}--closed`)
          nav.classList.remove('nav--light')
          nav.classList.add('nav--dark')
          navigation.classList.add('hidden')
          navigation.classList.remove('md:flex')
        } else {
          if (classButton === classButton) {
            navMenuReturn.classList.add('menu__return--show')
            navMenuReturn.classList.remove('menu__return--hide')
            // navMenuHamburger.classList.add('hamburger--hide')
            // navMenuHamburger.classList.remove('hamburger--show')
          } else {
            item.classList.add(`${classContent}--closed`)
            item.classList.remove(`${classContent}--opened`)
            nav.classList.remove('nav--dark')
            nav.classList.remove('nav--light')
            nav.classList.add(originalHeaderColor)
            logo.src = originalLogo
          }
        }
      });

      navMenuReturn.addEventListener('click', () => {
        navMenuReturn.classList.add('menu__return--hide')
        navMenuReturn.classList.remove('menu__return--show')
        navMenuHamburger.classList.add('hamburger--show')
        navMenuHamburger.classList.remove('hamburger--hide')
        item.classList.add(`${classContent}--closed`)
        item.classList.remove(`${classContent}--opened`)
        nav.classList.remove('nav--dark')
        nav.classList.remove('nav--light')
        nav.classList.add(originalHeaderColor)
        logo.src = originalLogo
        navigation.classList.add('hidden')
        navigation.classList.add('md:flex')
        document.body.style.overflow = 'initial'
      });
    });
  }

  revealMenu('hamburger','hamburger__content');
  revealMenu('hamburger-mobile','hamburger__content');

  function toggleScroll() {
    document.body.style.overflow == 'hidden'
      ? document.body.style.overflow = 'initial'
      : document.body.style.overflow = 'hidden'
  }

  function stopScroll() { document.body.style.overflow = 'hidden' }
  function startScroll() { document.body.style.overflow = 'initial' }

  // PRODUCT DRAG ACTION
  let draggableItems = document.querySelectorAll('.product-grid--draggable')
  let lastCursorX = null
  draggableItems.forEach((element) => {
    element.addEventListener("touchstart", elementStateHandler, false)
    element.addEventListener("touchend", elementStateHandler, false)
    element.addEventListener("touchmove", moveHandler, false)

    element.isActive = false
    element.addEventListener("mousedown", elementStateHandler, false)
    element.addEventListener("mouseup", elementStateHandler, false)
    element.addEventListener("mousemove", moveHandler, false)
  })

  function elementStateHandler(event) {
    let target = event.currentTarget
    if (event.type == "mousedown" || event.type == "touchstart") {
      target.isActive = true
      return
    }

    if (event.type == "mouseup" || event.type == "touchend") {
      target.isActive = false
      lastCursorX = null
      return
    }
  }

  function moveHandler(event) {
    let target = event.currentTarget
    if (event.type == "touchmove") currentXPos = event.touches[0].clientX
    if (event.type == "mousemove") currentXPos = event.clientX
    if (target.isActive) {
      if (window.innerWidth > 768) return
      if (lastCursorX == null) {
        lastCursorX = currentXPos
        return
      }
      let xCursorDif = currentXPos - lastCursorX
      if (xCursorDif > 0 || xCursorDif < 0) stopScroll()
      lastCursorX = currentXPos

      const translateX = new WebKitCSSMatrix(target.style.transform).e
      const newValue = translateX + (xCursorDif*2)
      if (newValue <= 0 && newValue >= (-1 * target.clientWidth + 300)) target.style.transform = `translateX(${newValue}px)`
      startScroll()
    }
  }

  // Reset the positioning when elements go from list (mobile) to desktop
  window.onresize = function() {
    if (window.innerWidth > 768)
      draggableItems.forEach(element => element.style.transform = `translateX(0px)`)
  }

  function listenerForCloseMessageOnClick() {
    let itemCloseMessage = document.querySelectorAll('.close-message');

    itemCloseMessage.forEach(function(item, index) {
      item.addEventListener('click', () => {
        let closeNumber = index + 1;
        let targetMessageId = `message-${closeNumber}`;
        let getElementToClose = document.getElementById(targetMessageId);
        if (getElementToClose !== null) {
          getElementToClose.classList.add('hidden');
        }
      });
    });
  }

  function closeMessagesInSeconds(seconds) {
    const time = seconds * 1000;
    var message_element = document.getElementById("message");
    if (message_element !== null) {
      setTimeout(function(){
        message_element.style.display = "none";
      }, time);
    };
  };

  closeMessagesInSeconds(10);
  listenerForCloseMessageOnClick();
}


// DOM aware start
docReady(kodiusWebsite());
