document.getElementById('loadMoreHistory').addEventListener('click', function () {
    const newHistory = document.createElement('div');
    newHistory.classList.add('history-item', 'd-flex', 'align-items-center', 'mb-3');
    newHistory.innerHTML = `
        <img src="https://images.unsplash.com/photo-1606813909026-9d3c51e3b6c3" alt="Watch">
        <div class="ms-3">
          <h6 class="mb-1">Luxury Watch</h6>
          <p class="text-muted mb-0">Purchased on Jun 2, 2024</p>
        </div>
      `;
    this.closest('.card').insertBefore(newHistory, this.parentElement);
    this.disabled = true;
    this.textContent = 'No More Orders';
});

document.getElementById('loadMoreCart').addEventListener('click', function () {
    document.getElementById('extraCartItem').classList.remove('d-none');
    this.disabled = true;
    this.textContent = 'All Items Loaded';
});