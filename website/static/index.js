console.log("hey");
$("input").click(function() {
  $(".form-control").animate({
    left: '250px',
    opacity: '1',
    height: '30px',
    width: '300px'
  });
});

$('.plus-cart').click(function(){
    console.log('Button clicked');

    var id = $(this).attr('pid').toString();
    var quantity = this.parentNode.children[2];

    $.ajax({
        type: 'GET',
        url: '/pluscart',
        data: {
            cart_id: id
        },
        success: function(data){
            console.log(data);
            if (data.success) {
                quantity.innerText = data.quantity;
                document.getElementById(`quantity${id}`).innerText = data.quantity;
                document.getElementById('amount_tt').innerText = data.amount;
                document.getElementById('totalamount').innerText = data.total;
            } else {
                alert(data.message);  // Display an alert with the error message
            }
        }
    });
});

$('.minus-cart').click(function(){
    console.log('Button clicked');

    var id = $(this).attr('pid').toString();
    var quantity = this.parentNode.children[2];

    $.ajax({
        type: 'GET',
        url: '/minuscart',
        data: {
            cart_id: id
        },
        success: function(data){
            console.log(data);
            if (data.success) {
                quantity.innerText = data.quantity;
                document.getElementById(`quantity${id}`).innerText = data.quantity;
                document.getElementById('amount_tt').innerText = data.amount;
                document.getElementById('totalamount').innerText = data.total;
            } else {
                alert(data.message);  // Display an alert with the error message
            }
        }
    });
});


$('.remove-cart').click(function(){
    var id = $(this).attr('pid').toString()
    var to_remove = this.parentNode.parentNode.parentNode.parentNode
    $.ajax({
        type: 'GET',
        url: '/removecart',
        data: {
            cart_id: id
        },
        success: function(data){
            document.getElementById('amount_tt').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total
            to_remove.remove()
        }
    })
})

/*
$('.add-likeness-points').click(function(){
    console.log('I was clicked!!!')
    var id = $(this).attr('pid').toString()
    $.ajax({
        type: 'GET',
        url: '/add-likeness-points',
        data: {
            product_id: id
        },
        success: function(data){
            document.getElementById(`pointsOfLikeness${id}`).innerText = data.likenessPoints
            location.reload(true);
            console.log(data)
        }
    })
})
*/
$('.fade').fadeIn(3000);

$(".btn-close").click(function(){
  $(".alert").hide();
});


$('.add-likeness-points').click(function() {
    console.log('I was clicked!!!');
    var id = $(this).attr('pid').toString();
    console.log('I was clicked1!!!');
    $.ajax({
        type: 'GET',
        url: '/add-likeness-points',
        data: {
            product_id: id
        },
        success: function(data) {
            console.log(id);
            console.log(data);
        },
        error: function(xhr, status, error) {
            console.error('Error occurred:', error);
            alert('An error occurred while adding likeness points.');
        }
    });
});

 document.addEventListener('DOMContentLoaded', function() {
        const carouselSlide = document.querySelector('.carousel-slide');
        const carouselImages = document.querySelectorAll('.promo-header img');

        let counter = 1;
        const size = carouselImages[0].clientWidth;

        carouselSlide.style.transform = 'translateX(' + (-size * counter) + 'px)';

        function moveCarousel() {
            if (counter >= carouselImages.length - 1) return;
            carouselSlide.style.transition = 'transform 0.4s ease-in-out';
            counter++;
            carouselSlide.style.transform = 'translateX(' + (-size * counter) + 'px)';
        }

        setInterval(() => {
            if (counter >= carouselImages.length - 1) {
                counter = -1;
            }
            moveCarousel();
        }, 3000); // Change slide every 3 seconds

        carouselSlide.addEventListener('transitionend', () => {
            if (carouselImages[counter].parentElement.id === 'lastClone') {
                carouselSlide.style.transition = 'none';
                counter = carouselImages.length - 2;
                carouselSlide.style.transform = 'translateX(' + (-size * counter) + 'px)';
            }
            if (carouselImages[counter].parentElement.id === 'firstClone') {
                carouselSlide.style.transition = 'none';
                counter = 1;
                carouselSlide.style.transform = 'translateX(' + (-size * counter) + 'px)';
            }
        });

        window.addEventListener('resize', () => {
            const newSize = carouselImages[0].clientWidth;
            carouselSlide.style.transition = 'none';
            carouselSlide.style.transform = 'translateX(' + (-newSize * counter) + 'px)';
        });
});

document.querySelectorAll('.toggle-btn').forEach(button => {
    button.addEventListener('click', () => {
        const description = button.nextElementSibling;
        description.style.display = description.style.display === 'none' ? 'block' : 'none';
    });
});


// With gsap thingy
/*
let text = document.querySelector(".text");

let animation = gsap.to(".image", {
  paused: true,
  opacity: 0
});

text.addEventListener("mouseenter", () => animation.play());
text.addEventListener("mouseleave", () => animation.reverse());
*/