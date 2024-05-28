/* eslint-disable sort-keys-plus/sort-keys */
/* eslint-disable prettier/prettier */
/* eslint-disable prefer-const */



// source : https://codepen.io/dadas190/pen/BYpEOa
let numbers = {
    red: [],
    black: [],
    green: []
};

window.sectors_values = {
    '1': [], // 1st row
    '2': [], // 2nd row
    '3': [], // 3rd row
    '4': [], // 1st 12
    '5': [], // 2nd 12
    '6': [], // 3rd 12
    '7': [], // 1 to 18
    '8': [], // EVEN
    '9': [], // RED
    '10': [], // BLACK
    '11': [], // ODD
    '12': [], // 19 to 36
}

/**
 * Get the html case of the wheels table based on the number
 * @param {Int} number
 * @returns {HTMLElement}
 */
function getCaseByNumber(number) {
    return Array.from(document.querySelectorAll(".roulette > table .num")).find(x => x.innerText == number);
}

//Simple fix
function initTable() {
        // init value on the colors
        console.log("ready");
        $(".roulette > table .num").each(function () {
            var $this = $(this),
                num = Number($this.text());
            for (var color in numbers) {
                if ($this.hasClass(color)) {
                    numbers[color].push(num);
                    $this.data('color', color);
                }
            }
        });

        // populate sectors
        for (var i = 1; i <= 36; i++) {
            // 1st row, 2nd row, 3rd row
            switch (i % 3) {
                case 0:
                    sectors_values['1'].push(i);
                    break;
                case 1:
                    sectors_values['3'].push(i);
                    break;
                case 2:
                    sectors_values['2'].push(i);
                    break;
            }

            // 1st 12, 2nd 12, 3rd 12
            if (i <= 12) {
                sectors_values['4'].push(i);
            } else if (i <= 24) {
                sectors_values['5'].push(i);
            } else {
                sectors_values['6'].push(i);
            }

            // 1 to 18, 19 to 36
            if (i <= 18) {
                sectors_values['7'].push(i);
            } else {
                sectors_values['12'].push(i);
            }

            // ODD, EVEN
            if (i % 2) {
                sectors_values['11'].push(i);
            } else {
                sectors_values['8'].push(i);
            }

            if (numbers.red.indexOf(i) != -1) {
                sectors_values['9'].push(i);
            } else if (numbers.black.indexOf(i) != -1) {
                sectors_values['10'].push(i);
            }
        }

        /* Set event hover on each case*/

        //For all number
        document.querySelectorAll(".controlls-2 .num").forEach(element => {
            $(element).hover(_ => {
                $(getCaseByNumber(element.dataset.num)).addClass("hover");
            }, _ => {
                $(getCaseByNumber(element.dataset.num)).removeClass("hover");
            })

            //Fix when hover exit
            $(element).on("mousemove", e => {
                $(getCaseByNumber(e.currentTarget.dataset.num)).addClass("hover");
            });
        });

        //For all sectors
        /*  document.querySelectorAll(".controlls-2 .sector").forEach((element, i) => {
              let sectors_number = element.dataset.sector;
              $(element).hover(_ => {
                  let allCaseNumber = sectors_values[sectors_number];
                  allCaseNumber.map(x => getCaseByNumber(x)).forEach(element => {
                      $(element).addClass("hover");
                  });
              }, _ => {
                  let allCaseNumber = sectors_values[sectors_number];
                  allCaseNumber.map(x => getCaseByNumber(x)).forEach(element => {
                      $(element).removeClass("hover");
                  });
              });

              //fix with mouse move
              if (sectors_number <= 6) {
                  $(element).on("mousemove", e => {
                      let allCaseNumber = sectors_values[sectors_number];
                      allCaseNumber.map(x => getCaseByNumber(x)).forEach(element => {
                          $(element).addClass("hover");
                      });
                  });
              }
          }); */

        //For all "a cheval bet" horizontal
        /* document.querySelectorAll(".controlls-2 .num .btn.v.cv").forEach(element => {
             $(element).hover(_ => {
                 let allCaseNumber = element.dataset.num.split(",");
                 allCaseNumber.map(x => getCaseByNumber(x)).forEach(element => {
                     $(element).addClass("hover");
                 });
             }, _ => {
                 let allCaseNumber = element.dataset.num.split(",");
                 allCaseNumber.map(x => getCaseByNumber(x)).forEach(element => {
                     $(element).removeClass("hover");
                 });
             });
         }); */

        //For all "a cheval bet" vertical
        /* document.querySelectorAll(".controlls-2 .num .btn.h.rh").forEach(element => {
             $(element).hover(_ => {
                 let allCaseNumber = element.dataset.num.split(",");
                 allCaseNumber.map(x => getCaseByNumber(x)).forEach(element => {
                     $(element).addClass("hover");
                 });
             }, _ => {
                 let allCaseNumber = element.dataset.num.split(",");
                 allCaseNumber.map(x => getCaseByNumber(x)).forEach(element => {
                     $(element).removeClass("hover");
                 });
             });
         }); */

        //For all square bet
        /*  document.querySelectorAll(".controlls-2 .btn.c.rh.lg").forEach(element => {
              $(element).hover(_ => {
                  let allCaseNumber = element.dataset.num.split(",");
                  allCaseNumber.map(x => getCaseByNumber(x)).forEach(element => {
                      $(element).addClass("hover");
                  });
              }, _ => {
                  let allCaseNumber = element.dataset.num.split(",");
                  allCaseNumber.map(x => getCaseByNumber(x)).forEach(element => {
                      $(element).removeClass("hover");
                  });
              });
          }); */

        //For all double columns or double douzaine
        /* document.querySelectorAll(".controlls-2 .sector .btn").forEach(element => {
             $(element).hover(_ => {
                 let allSectorNumber = element.dataset.sector.split(",");
                 let allCaseNumber = sectors_values[allSectorNumber[0]].concat(sectors_values[allSectorNumber[1]])
                 allCaseNumber.map(x => getCaseByNumber(x)).forEach(element => {
                     $(element).addClass("hover");
                 });
             }, _ => {
                 let allSectorNumber = element.dataset.sector.split(",");
                 let allCaseNumber = sectors_values[allSectorNumber[0]].concat(sectors_values[allSectorNumber[1]])
                 allCaseNumber.map(x => getCaseByNumber(x)).forEach(element => {
                     $(element).removeClass("hover");
                 });
             });
         }); */

}



function drawChip(elementClicked, value, isOwnBet, username) {
    let colorChip = "blue";
    if (value >= 5) {
        colorChip = "orange"
    }
    if (value >= 10) {
        colorChip = "purple"
    }
    if (value >= 25) {
        colorChip = "red"
    }
    if (value >= 50) {
        colorChip = "gold"
    }


    let chip = `<div class="chip-container ${isOwnBet ? "" : "online"}"><div class="chip ${colorChip}" style=""><span class="chipSpan">${value}</span><span style="display: none;">${username}</span></div></div>`;
    var wrapper = document.createElement('div');
    wrapper.innerHTML = chip;
    let img = wrapper.firstChild;
    img.style.zIndex = "0";
    img.style.position = "absolute";

    document.querySelector(".chips").appendChild(img);
    let widthChip = img.clientWidth;
    let heightChip = img.clientHeight;
    img.style.left = (getCasePositionRelativeOfBody(elementClicked, widthChip, heightChip).left) + "px";
    img.style.top = ((getCasePositionRelativeOfBody(elementClicked, widthChip, heightChip).top) - 64) + "px";
    img.style.pointerEvents = "none";
}


function getCasePositionRelativeOfBody(elementClicked, widthChip, heightChip) {
    if ($(elementClicked).hasClass("sector")) {
        return {
            left: elementClicked.getBoundingClientRect().left + (widthChip / 4),
            top: elementClicked.getBoundingClientRect().top + (heightChip / 4)
        }
    }
    if ($(elementClicked).hasClass("num")) {
        return {
            left: elementClicked.getBoundingClientRect().left + (widthChip / 4),
            top: elementClicked.getBoundingClientRect().top + (heightChip / 4)
        }
    }
    if ($(elementClicked).hasClass("btn")) {
        if ($(elementClicked).hasClass("v")) {
            return {
                left: elementClicked.getBoundingClientRect().left - (widthChip / 4),
                top: elementClicked.getBoundingClientRect().top
            }
        }
        if ($(elementClicked).hasClass("h")) {
            return {
                left: elementClicked.getBoundingClientRect().left,
                top: elementClicked.getBoundingClientRect().top - (heightChip / 4)
            }
        }
        if ($(elementClicked).hasClass("c")) {
            return {
                left: elementClicked.getBoundingClientRect().left - (widthChip / 4),
                top: elementClicked.getBoundingClientRect().top - (heightChip / 4)
            }
        }
    }
}

function getColorOfNumber(number)
{
    if(number == 0)
        return "green"
    let caseHtml = getCaseByNumber(number);
    let classList = caseHtml.classList.value.split(",").toString().replace("num","");
    return classList.trim();
}


window.updateBetsView = (bets, userLogged) => {
    $(".locked").removeClass("locked")
    document.querySelector(".chips").innerHTML = "";
    bets.forEach((value, key) => {
        let isOwnBet = (userLogged == value.userId) ? true : false;
        drawChip(value.htmlElement, value.value, isOwnBet, value.userId);
        let numberSelected;
        if (key.split("-")[0] == "num") {
            numberSelected = key.split("-")[1].split(",");
        }
        else {
            let dataSelected = key.split("-")[1].split(",")
            numberSelected = dataSelected.map(x => sectors_values[x]).flat();
        }
        numberSelected.forEach(number => {
            let el = getCaseByNumber(number)
            $(el).addClass("locked")
        })
    });
}

