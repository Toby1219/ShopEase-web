document.getElementById('reviewForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const review = document.getElementById('review').value;

    const reviewBox = document.createElement('div');
    reviewBox.classList.add('review-box');
    reviewBox.innerHTML = `<strong>${name}</strong> <span class="text-warning">★★★★★</span><p>${review}</p>`;

    this.insertAdjacentElement('beforebegin', reviewBox);
    this.reset();
});