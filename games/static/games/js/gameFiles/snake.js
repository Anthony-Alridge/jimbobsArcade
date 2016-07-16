/*Contain code for the snake game (own code)*/

//global variables
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

var gridSize = 10;
var x_block_count = canvas.width/gridSize;
var y_block_count = canvas.height/gridSize;
var x_mid = (x_block_count/2) * gridSize;
var y_mid = (y_block_count/2) * gridSize;

var snake = [];
snake[0] = {x:x_mid, y:y_mid};
var snakeSize = 1;

var r = 1;
var l = 0;
var u = 0;
var d = 0;

var food = 0;
var foodX = 0;
var foodY = 0;

var score = 0;

//collison functions
function intersectRect(r1, r2) {
  return !(r2.left > r1.right ||
           r2.right < r1.left ||
           r2.top > r1.bottom ||
           r2.bottom < r1.top);
}
function addBody(){
  tail = snake[snake.length-1];
  if(u){
    body = {x:tail.x ,y:tail.y+gridSize}
  }else if(d){
    body = {x:tail.x, y:tail.y-gridSize}
  }else if(l){
    body = {x:tail.x + gridSize, y:tail.y}
  }else if(r){
    body = {x:tail.x - gridSize, y:tail.y}
  }
  snake.push(body);
}

  function eatFood(){
    var head = snake[0];
    if(head.x > foodX && head.x < foodX+gridSize*2 && head.y > foodY && head.y < foodY+gridSize*2){
      food = 0;
      score ++;
      addBody();
      addBody();
      addBody();
    }
  }

  function eatSelf(){
    var head = snake[0]
    for( b = 1; b < snake.length;b++){
        if(head.x == snake[b].x && head.y == snake[b].y){
          document.location.reload();
        }
    }
  }

function collisonHandler(){
  eatFood();
  eatSelf();
}
//motion
  function snakeMotion(){
    var head = snake[0];
    headX = head.x;
    headY = head.y;
    if(r){
      //moving right
      if(head.x+gridSize > canvas.width){
        snake.unshift({x:0, y:headY});
      }else{
        snake.unshift({x:headX+gridSize, y:headY});
    }
    }else if(l){
      //moving left
      if(head.x < 0){
        snake.unshift({x:canvas.width, y:headY});
      }else{
        snake.unshift({x:headX-gridSize, y:headY});
    }
    }else if(u){
      //moving up
      if(head.y < 0){
        snake.unshift({x:headX, y:canvas.height});
      }else{
        snake.unshift({x:headX, y:headY-gridSize});
    }
    }else{
      //moving down
      if(head.y + gridSize > canvas.height){
        snake.unshift({x:headX, y:0});
      }else{
        snake.unshift({x:headX, y:headY+gridSize});
    }
    }
    snake.pop();

  }
//drawing functions
  function drawSnake(){
    //loop through each entry in the snake array and draw a sqaure at the grid
    //locaton represented by those co-ordanates.
    snakeMotion();
    for(b in snake){
      var xCo = snake[b].x;
      var yCo = snake[b].y;
      ctx.beginPath();
      ctx.rect(xCo, yCo, gridSize, gridSize);
      ctx.fillStyle = "#0095DD";
      ctx.fill();
      ctx.closePath();
    }


  }

  function drawFood(){
    //spawn a food item at a random place in the grid when the previous
    //one is eaten
    if(!food){
      food = 1;
      foodX = Math.random()*canvas.width;
      foodY = Math.random()*canvas.height;
      ctx.beginPath();
      ctx.rect(foodX, foodY, gridSize, gridSize);
      ctx.fillStyle = "#009900";
      ctx.fill();
      ctx.closePath();
    }else{
      ctx.beginPath();
      ctx.rect(foodX, foodY, gridSize*2, gridSize*2);
      ctx.fillStyle = "#009900";
      ctx.fill();
      ctx.closePath();

    }
  }
  function drawScore() {
      ctx.font = "16px Arial";
      ctx.fillStyle = "#0095DD";
      ctx.fillText("Score: "+score, 8, 20);
  }
//other

function main(){
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawSnake();
  drawFood();
  drawScore();
  collisonHandler();
}
//key events
function keyDownHandler(e) {
    if(e.keyCode == 39) {
        r = 1;
        l = u = d = 0;
    }
    else if(e.keyCode == 37) {
        l = 1;
        r = u = d = 0;
    }
    else if(e.keyCode == 38){
        u = 1;
        r = l = d = 0;
    }
    else if(e.keyCode == 40){
        d = 1;
        r = l = u = 0;
    }
}

function keyUpHandler(e) {
    if(e.keyCode == 39) {
        rightPressed = false;
    }
    else if(e.keyCode == 37) {
        leftPressed = false;
    }
}
document.addEventListener("keydown", keyDownHandler, false);

setInterval(main, 60);
