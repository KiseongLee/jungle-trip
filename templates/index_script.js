const cardBox = $('.card-box')    
    
    function onClickLike(city){
      $.ajax({
        type : "POST",
        url : "/like",
        data : {'city' : city},
        success : res => {
          if(res['result'] === 'success'){
            window.location.reload()
          }
        }
      })
    }    

    $('.login__button').click(()=>{
      window.location.href='./login';
    })
    
    $('.myPage__button').click(()=>{
      window.location.href='./mypage';
    })

function logout(){
        $.removeCookie('mytoken');
        alert('로그아웃!')
        window.location.href='/'}

    $.ajax({
      type : "GET",
      url : "/read",
      data : {},
      success : (res)=>{
        if(res['result'] === "success"){
          res['cities'].map((data)=>{
            makeCard(data)
          })
        }
      }
    })
  
    function makeCard(data){
      const card = `<li class="card">
        <img class = "card__image" src="${data['image']}">         
        <div class="text"><b>${data['city']}</b></div>   
        <button class="like__button" onclick="onClickLike('${data['city']}')">
          <i class="fa-solid fa-heart"></i>
          <span class="likeButtonNum">${data['like']}</span>
        </button>
        <div class="description">${data['desc']}</div>      
    </li>`
      cardBox.append(card)
    }