document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.like_button').forEach(button => {
      button.addEventListener('click', function (event) {
        event.preventDefault();
        const itemId = this.dataset.itemId;
        fetch(`/like-item/${itemId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
          }
        })
        .then(response => response.json())
        .then(data => {
          if (data.error) {
            alert(data.error);
          } else {
            const likeCountElem = document.querySelector(`#like-count-${itemId}`);
            likeCountElem.textContent = data.likes_count;
            this.textContent = data.liked ? 'Unlike' : 'Like';
          }
        });
      });
    });
  });
  