document.addEventListener('DOMContentLoaded', function() {
    const followBtn = document.getElementById('follow-btn');
    const csrfToken = document.getElementById('csrf-token').value;

    if (followBtn) {
        followBtn.addEventListener('click', function(event) {
            event.preventDefault();

            const url = followBtn.getAttribute('href');

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
                credentials: 'same-origin',
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_following) {
                    followBtn.textContent = 'Following';
                } else {
                    followBtn.textContent = 'Follow';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});
// $(document).ready(function(){
//     $('#follow-btn').click(function(event){
//         event.preventDefault();

//         var url = $(this).attr('href');
//         var csrfToken = $('input[name=csrfmiddlewaretoken]').val();

//         $.ajax({
//             url: url,
//             type: 'POST',
//             headers: {
//                 'X-CSRFToken': csrfToken
//             },
//             success: function(response) {
//                 if (response.is_following) {
//                     $('#follow-btn').text('Following');
//                 } else {
//                     $('#follow-btn').text('Follow');
//                 }
//             },
//             error: function(xhr, status, error) {
//                 console.error('AJAX request failed:', status, error);
//             }
//         });
//     });
// });