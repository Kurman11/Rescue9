//  댓글 좋아요 비동기
const reviewLikeForm = document.querySelectorAll('.review-like-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

reviewLikeForm.forEach(form => {
  form.addEventListener('submit', function (event) {
  event.preventDefault()
  const reviewId = event.target.dataset.reviewId
  const recipeId = event.target.dataset.recipeId
  // console.log(event.target.dataset)
  axios({
    method: 'post',
    url: `/recipes/${recipeId}/reviews/${reviewId}/like/`,
    headers: {'X-CSRFToken': csrftoken},
  })
    .then((response) => {
      // console.log(response.data)
      const isLiked = response.data.is_liked
      const likeBtnIcon = document.querySelector(`#review-like-form-${reviewId} > button > i`)

      if (isLiked === true) {
        likeBtnIcon.setAttribute('class', 'bi bi-heart-fill me-1')
      } else {
        likeBtnIcon.setAttribute('class', 'bi bi-heart me-1')
      }

      const likesCountTag = document.querySelector(`#likesCountTag-${reviewId}`)
      
      const likesCountTagData = response.data.likes_count

      // 선택한 span 태그의 내용을 팔로잉과 팔로워 수로 채워넣기
      likesCountTag.textContent = likesCountTagData
    })
  })
})


// 별점 관련
var currentRating = 0;
var stars = document.querySelectorAll('.star-rating .star')

function fillStars(el) {
  // 호버한 별과 그 앞의 모든 별을 채운다.
  var rating = el.getAttribute('data-value')
  for (var i = 0; i < stars.length; i++) {
    if (i < rating) {
      stars[i].classList.add('filled')
    } else {
      stars[i].classList.remove('filled')
    }
  }
}

function setRating(el) {
  // 클릭한 별과 그 앞의 모든 별을 채운다.
  var rating = el.getAttribute('data-value')
  for (var i = 0; i < stars.length; i++) {
    if (i < rating) {
      stars[i].classList.add('selected')
    } else {
      stars[i].classList.remove('selected')
    }
  }
  currentRating = rating;

  // rating 값을 form의 rating input 요소에 할당
  var ratingInput = document.querySelector('input[name=rating]')
  ratingInput.value = rating
}

function unfillStars() {
  // 모든 별을 검은색으로 변경한다.
  for (var i = 0; i < stars.length; i++) {
    stars[i].classList.remove('filled')
  }
}

// 이벤트 리스너 추가
var starRating = document.querySelector('.star-rating');
starRating.addEventListener('mouseover', function(e) {
  if (e.target.classList.contains('star')) {
    fillStars(e.target);
  }
})

starRating.addEventListener('mouseout', function(e) {
  if (e.target.classList.contains('star')) {
    unfillStars();
  }
})

starRating.addEventListener('click', function(e) {
  if (e.target.classList.contains('star')) {
    setRating(e.target);
  }
})


// 사진 업로드 미리보기
function previewImages(event) {
  var input = event.target;
  var preview = document.getElementById('preview');
  preview.innerHTML = ''; // clear previous preview images
  if (input.files && input.files.length > 0) {
      for (var i = 0; i < input.files.length; i++) {
          var reader = new FileReader();
          reader.onload = function(e) {
              var img = document.createElement('img');
              img.src = e.target.result;
              img.className = 'thumbnail';
              
              var closeBtn = document.createElement('button');
              closeBtn.innerText = 'x';
              closeBtn.className = 'close-btn';
              closeBtn.onclick = function() {
                  preview.removeChild(wrapper);
                  input.value = ''; // reset the file input to allow re-selection of the same file
              }
              
              var wrapper = document.createElement('div');
              wrapper.className = 'thumbnail-wrapper';
            wrapper.appendChild(closeBtn);
              wrapper.appendChild(img);
              preview.appendChild(wrapper);
          }
          reader.readAsDataURL(input.files[i]);
      }
  }
}


// 작성된 포토리뷰 
// 모달 창이 켜졌을 때 closeModal 실행 
window.addEventListener("click", function(event) {
  var modal = document.getElementById("modal");
  if (event.target === modal) {
    closeModal();
  }
});

// 이미지를 눌렀을 경우 모달창 켜기
function openModal(imageUrl, content, username) {
  console.log(imageUrl)
  console.log(content)
  var modal = document.getElementById("modal");
  var modalImage = document.getElementById("modalImage");
  var modalContent = document.getElementById("modalContent");
  var modalUser = document.getElementById("modalUser");
  modal.style.display = "block";
  modalImage.src = imageUrl;
  modalContent.textContent = content;
  modalUser.textContent = username;
}
// 모달 창 끄기
function closeModal() {
  var modal = document.getElementById("modal");
  modal.style.display = "none";
}

$('#recipeDeleteModal').modal('show').on('shown.bs.modal', function() {
  $('recipeDeleteModal').focus();
});


// 리뷰 삭제
function deleteReview(event, recipe_pk, review_pk) {
  event.preventDefault();
  if (confirm('리뷰를 삭제하시겠습니까?')) {
    fetch(`/recipes/${recipe_pk}/reviews/${review_pk}/review_delete/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': csrftoken,
      },
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('서버 에러');
      }
    })
    .then(data => {
      if (data.status === 'ok') {
        // Reload the page to reflect the updated reviews
        location.reload();
      } else {
        alert(data.message);
      }
    })
    .catch(error => {
      alert(error.message);
    });
  }
}