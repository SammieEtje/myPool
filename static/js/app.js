// F1 Betting Pool - Single Page Application
// ============================================

const app = {
  currentUser: null,
  currentPage: 'competitions',
  selectedDrivers: [],
  drivers: [],
  competitions: [],

  // Initialize app
  init() {
    this.checkAuth();
    this.setupNavigation();
    this.loadPage('competitions');
  },

  // Check authentication status
  async checkAuth() {
    try {
      const response = await fetch('/api/profiles/me/', {
        credentials: 'include'
      });

      if (response.ok) {
        this.currentUser = await response.json();
        this.renderAuthSection();
      } else {
        this.renderAuthSection();
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      this.renderAuthSection();
    }
  },

  // Render authentication section
  renderAuthSection() {
    const authSection = document.getElementById('authSection');

    if (this.currentUser) {
      authSection.innerHTML = `
        <div class="user-avatar" title="${this.currentUser.email}">
          ${this.currentUser.display_name ? this.currentUser.display_name.charAt(0).toUpperCase() :
            this.currentUser.email.charAt(0).toUpperCase()}
        </div>
        <span style="color: var(--color-text-secondary);">
          ${this.currentUser.total_points} pts
        </span>
        <a href="/accounts/logout/" class="btn btn-sm btn-ghost">Logout</a>
      `;
    } else {
      authSection.innerHTML = `
        <a href="/accounts/login/" class="btn btn-sm btn-primary">Login</a>
        <a href="/accounts/signup/" class="btn btn-sm btn-outline">Sign Up</a>
      `;
    }
  },

  // Setup navigation
  setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const page = link.dataset.page;

        // Update active state
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');

        this.loadPage(page);
      });
    });
  },

  // Load page content
  loadPage(page) {
    this.currentPage = page;
    const content = document.getElementById('appContent');

    switch(page) {
      case 'competitions':
        this.loadCompetitionsPage();
        break;
      case 'races':
        this.loadRacesPage();
        break;
      case 'my-bets':
        this.loadMyBetsPage();
        break;
      case 'leaderboard':
        this.loadLeaderboardPage();
        break;
    }
  },

  // Load competitions page
  async loadCompetitionsPage() {
    const template = document.getElementById('template-competitions');
    const content = document.getElementById('appContent');
    content.innerHTML = template.innerHTML;

    const loading = document.getElementById('competitionsLoading');
    const list = document.getElementById('competitionsList');
    const empty = document.getElementById('competitionsEmpty');

    loading.classList.remove('hidden');

    try {
      const response = await fetch('/api/competitions/', {
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        // Handle paginated response (DRF returns {results: [...], count: N})
        const competitions = data.results || data;
        this.competitions = competitions;
        loading.classList.add('hidden');

        if (competitions.length === 0) {
          empty.classList.remove('hidden');
        } else {
          list.innerHTML = '';
          competitions.forEach(comp => {
            const card = this.createCompetitionCard(comp);
            list.appendChild(card);
          });
        }
      }
    } catch (error) {
      console.error('Failed to load competitions:', error);
      loading.classList.add('hidden');
      empty.classList.remove('hidden');
    }
  },

  // Create competition card
  createCompetitionCard(competition) {
    const template = document.getElementById('template-competition-card');
    const card = template.content.cloneNode(true);

    card.querySelector('.competition-status').textContent = competition.status;
    card.querySelector('.competition-card-year').textContent = competition.year;
    card.querySelector('.competition-name').textContent = competition.name;
    card.querySelector('.competition-description').textContent = competition.description || 'No description';
    card.querySelector('.competition-races-count').textContent = competition.races_count || 0;
    card.querySelector('.competition-participants-count').textContent = competition.participants_count || 0;

    const joinBtn = card.querySelector('.btn-join-competition');
    joinBtn.dataset.competitionId = competition.id;
    joinBtn.addEventListener('click', () => this.joinCompetition(competition.id));

    const viewBtn = card.querySelector('.btn-view-competition');
    viewBtn.dataset.competitionId = competition.id;
    viewBtn.addEventListener('click', () => this.viewCompetition(competition.id));

    return card;
  },

  // Join competition
  async joinCompetition(competitionId) {
    if (!this.currentUser) {
      alert('Please login to join a competition');
      window.location.href = '/accounts/login/';
      return;
    }

    try {
      const response = await fetch(`/api/competitions/${competitionId}/join/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCookie('csrftoken')
        }
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message || 'Successfully joined competition!');
        this.loadCompetitionsPage();
      } else {
        alert(data.error || 'Failed to join competition');
      }
    } catch (error) {
      console.error('Failed to join competition:', error);
      alert('Failed to join competition');
    }
  },

  // View competition details
  viewCompetition(competitionId) {
    // Navigate to leaderboard for this competition
    this.loadLeaderboardPage(competitionId);

    // Update nav
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    document.querySelector('.nav-link[data-page="leaderboard"]').classList.add('active');
  },

  // Load races page
  async loadRacesPage() {
    const template = document.getElementById('template-races');
    const content = document.getElementById('appContent');
    content.innerHTML = template.innerHTML;

    // Load competitions for filter
    await this.loadCompetitionsFilter('raceFilterCompetition');

    const loading = document.getElementById('racesLoading');
    const list = document.getElementById('racesList');
    const empty = document.getElementById('racesEmpty');

    loading.classList.remove('hidden');

    try {
      const response = await fetch('/api/races/?upcoming=true', {
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        const races = data.results || data;
        loading.classList.add('hidden');

        if (races.length === 0) {
          empty.classList.remove('hidden');
        } else {
          list.innerHTML = '';
          races.forEach(race => {
            const card = this.createRaceCard(race);
            list.appendChild(card);
          });
        }
      }
    } catch (error) {
      console.error('Failed to load races:', error);
      loading.classList.add('hidden');
      empty.classList.remove('hidden');
    }
  },

  // Create race card
  createRaceCard(race) {
    const template = document.getElementById('template-race-card');
    const card = template.content.cloneNode(true);

    const cardElement = card.querySelector('.race-card');
    if (race.is_betting_open) {
      cardElement.classList.add('betting-open');
    } else {
      cardElement.classList.add('betting-closed');
    }

    card.querySelector('.race-round').textContent = `Round ${race.round_number}`;
    card.querySelector('.race-name').textContent = race.name;
    card.querySelector('.race-location').textContent = `${race.location}, ${race.country}`;
    card.querySelector('.race-datetime').textContent = new Date(race.race_datetime).toLocaleString();
    card.querySelector('.race-deadline-text').textContent = `Betting closes: ${new Date(race.betting_deadline).toLocaleString()}`;

    const statusBadge = card.querySelector('.race-status-badge');
    statusBadge.textContent = race.status;
    statusBadge.className = `badge ${race.is_betting_open ? 'badge-success' : 'badge-error'}`;

    const betBtn = card.querySelector('.btn-place-bet');
    betBtn.dataset.raceId = race.id;
    if (race.is_betting_open && this.currentUser) {
      betBtn.addEventListener('click', () => this.openBettingModal(race));
    } else {
      betBtn.disabled = true;
      betBtn.textContent = race.is_betting_open ? 'Login to Bet' : 'Betting Closed';
    }

    const resultsBtn = card.querySelector('.btn-view-results');
    resultsBtn.dataset.raceId = race.id;
    resultsBtn.addEventListener('click', () => this.viewRaceResults(race.id));

    return card;
  },

  // Load leaderboard page
  async loadLeaderboardPage(competitionId = null) {
    const template = document.getElementById('template-leaderboard');
    const content = document.getElementById('appContent');
    content.innerHTML = template.innerHTML;

    await this.loadCompetitionsFilter('leaderboardFilterCompetition');

    const filter = document.getElementById('leaderboardFilterCompetition');
    if (competitionId) {
      filter.value = competitionId;
    }

    filter.addEventListener('change', (e) => {
      if (e.target.value) {
        this.loadLeaderboard(e.target.value);
      }
    });

    if (filter.value) {
      this.loadLeaderboard(filter.value);
    }
  },

  // Load leaderboard data
  async loadLeaderboard(competitionId) {
    const loading = document.getElementById('leaderboardLoading');
    const list = document.getElementById('leaderboardList');
    const empty = document.getElementById('leaderboardEmpty');

    loading.classList.remove('hidden');
    list.innerHTML = '';

    try {
      const response = await fetch(`/api/standings/?competition=${competitionId}`, {
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        const standings = data.results || data;
        loading.classList.add('hidden');

        if (standings.length === 0) {
          empty.classList.remove('hidden');
        } else {
          empty.classList.add('hidden');
          standings.forEach(standing => {
            const item = this.createLeaderboardItem(standing);
            list.appendChild(item);
          });
        }
      }
    } catch (error) {
      console.error('Failed to load leaderboard:', error);
      loading.classList.add('hidden');
      empty.classList.remove('hidden');
    }
  },

  // Create leaderboard item
  createLeaderboardItem(standing) {
    const template = document.getElementById('template-leaderboard-item');
    const item = template.content.cloneNode(true);

    item.querySelector('.leaderboard-rank').textContent = `#${standing.rank}`;
    item.querySelector('.leaderboard-name').textContent = standing.user_display_name || standing.user_email;
    item.querySelector('.stat-exact-predictions').textContent = `${standing.exact_predictions} exact`;
    item.querySelector('.stat-races-predicted').textContent = `${standing.races_predicted} races`;
    item.querySelector('.leaderboard-points').textContent = `${standing.total_points} pts`;

    return item;
  },

  // Load my bets page
  async loadMyBetsPage() {
    if (!this.currentUser) {
      alert('Please login to view your bets');
      window.location.href = '/accounts/login/';
      return;
    }

    const template = document.getElementById('template-my-bets');
    const content = document.getElementById('appContent');
    content.innerHTML = template.innerHTML;

    await this.loadCompetitionsFilter('myBetsFilterCompetition');

    const loading = document.getElementById('myBetsLoading');
    const list = document.getElementById('myBetsList');
    const empty = document.getElementById('myBetsEmpty');

    loading.classList.remove('hidden');

    try {
      const response = await fetch('/api/bets/my_bets/', {
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        const bets = data.results || data;
        loading.classList.add('hidden');

        if (bets.length === 0) {
          empty.classList.remove('hidden');
        } else {
          list.innerHTML = '<div class="table"><table style="width:100%"><thead><tr><th>Race</th><th>Driver</th><th>Predicted Position</th><th>Points</th><th>Status</th></tr></thead><tbody id="myBetsTableBody"></tbody></table></div>';

          const tbody = document.getElementById('myBetsTableBody');
          bets.forEach(bet => {
            const row = document.createElement('tr');
            row.innerHTML = `
              <td>${bet.race_name}</td>
              <td>${bet.driver_name}</td>
              <td>P${bet.predicted_position}</td>
              <td>${bet.points_earned}</td>
              <td><span class="badge ${bet.is_scored ? 'badge-success' : 'badge-warning'}">${bet.is_scored ? 'Scored' : 'Pending'}</span></td>
            `;
            tbody.appendChild(row);
          });
        }
      }
    } catch (error) {
      console.error('Failed to load bets:', error);
      loading.classList.add('hidden');
      empty.classList.remove('hidden');
    }
  },

  // Load competitions filter
  async loadCompetitionsFilter(selectId) {
    const select = document.getElementById(selectId);
    if (!select) return;

    try {
      const response = await fetch('/api/competitions/', {
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        const competitions = data.results || data;
        competitions.forEach(comp => {
          const option = document.createElement('option');
          option.value = comp.id;
          option.textContent = `${comp.year} - ${comp.name}`;
          select.appendChild(option);
        });
      }
    } catch (error) {
      console.error('Failed to load competitions:', error);
    }
  },

  // Open betting modal
  async openBettingModal(race) {
    if (!this.currentUser) {
      alert('Please login to place bets');
      window.location.href = '/accounts/login/';
      return;
    }

    this.selectedDrivers = [];
    this.currentRace = race;

    // Load drivers if not already loaded
    if (this.drivers.length === 0) {
      await this.loadDrivers();
    }

    const template = document.getElementById('template-betting-modal');
    const modal = template.content.cloneNode(true);
    document.body.appendChild(modal);

    document.querySelector('.race-modal-name').textContent = race.name;

    const driverSelector = document.getElementById('driverSelector');
    this.drivers.forEach(driver => {
      const driverCard = document.createElement('div');
      driverCard.className = 'driver-option';
      driverCard.dataset.driverId = driver.id;
      driverCard.innerHTML = `
        <div class="driver-number">${driver.driver_number}</div>
        <div class="driver-info">
          <div class="driver-name">${driver.first_name} ${driver.last_name}</div>
          <div class="driver-team">${driver.team}</div>
        </div>
      `;

      driverCard.addEventListener('click', () => this.toggleDriver(driver, driverCard));
      driverSelector.appendChild(driverCard);
    });
  },

  // Load drivers
  async loadDrivers() {
    try {
      const response = await fetch('/api/drivers/', {
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        this.drivers = data.results || data;
      }
    } catch (error) {
      console.error('Failed to load drivers:', error);
    }
  },

  // Toggle driver selection
  toggleDriver(driver, element) {
    const index = this.selectedDrivers.findIndex(d => d.id === driver.id);

    if (index > -1) {
      // Remove driver
      this.selectedDrivers.splice(index, 1);
      element.classList.remove('selected');
    } else {
      // Add driver
      if (this.selectedDrivers.length < 10) {
        this.selectedDrivers.push(driver);
        element.classList.add('selected');
      } else {
        alert('You can only select 10 drivers');
        return;
      }
    }

    this.updateSelectedDriversList();
  },

  // Update selected drivers list
  updateSelectedDriversList() {
    const list = document.getElementById('selectedDriversList');

    if (this.selectedDrivers.length === 0) {
      list.innerHTML = '<p class="text-muted">No drivers selected yet. Select up to 10 drivers.</p>';
      return;
    }

    list.innerHTML = '<div style="display: flex; flex-direction: column; gap: 0.5rem;">';
    this.selectedDrivers.forEach((driver, index) => {
      const item = document.createElement('div');
      item.style.cssText = 'display: flex; align-items: center; gap: 1rem; padding: 0.5rem; background: var(--color-dark-700); border-radius: 8px;';
      item.innerHTML = `
        <span style="font-weight: 900; min-width: 30px;">P${index + 1}</span>
        <span style="flex: 1;">#${driver.driver_number} ${driver.first_name} ${driver.last_name}</span>
      `;
      list.appendChild(item);
    });
    list.innerHTML += '</div>';
  },

  // Submit bet
  async submitBet() {
    if (this.selectedDrivers.length !== 10) {
      alert('Please select exactly 10 drivers');
      return;
    }

    const predictions = this.selectedDrivers.map((driver, index) => ({
      driver: driver.id,
      position: index + 1
    }));

    try {
      // Get the default "Top 10" bet type
      const betTypesResponse = await fetch('/api/bet-types/', {
        credentials: 'include'
      });

      const betTypes = await betTypesResponse.json();
      const top10BetType = betTypes.find(bt => bt.code === 'top10');

      if (!top10BetType) {
        alert('Bet type not found. Please contact administrator.');
        return;
      }

      const response = await fetch('/api/bets/bulk_create/', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCookie('csrftoken')
        },
        body: JSON.stringify({
          race: this.currentRace.id,
          bet_type: top10BetType.id,
          predictions: predictions
        })
      });

      if (response.ok) {
        alert('Bet placed successfully!');
        this.closeBettingModal();
        this.loadPage('my-bets');
      } else {
        const error = await response.json();
        alert('Failed to place bet: ' + (error.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Failed to submit bet:', error);
      alert('Failed to place bet');
    }
  },

  // Close betting modal
  closeBettingModal() {
    const modal = document.getElementById('bettingModal');
    if (modal) {
      modal.remove();
    }
    this.selectedDrivers = [];
  },

  // View race results
  async viewRaceResults(raceId) {
    try {
      const response = await fetch(`/api/races/${raceId}/results/`, {
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        const results = data.results || data;

        if (results.length === 0) {
          alert('Results not available yet');
          return;
        }

        let resultsHTML = '<h3>Race Results</h3><div class="table"><table style="width:100%"><thead><tr><th>Pos</th><th>Driver</th><th>Team</th></tr></thead><tbody>';

        results.forEach(result => {
          const driver = result.driver_name.split(' ');
          resultsHTML += `
            <tr>
              <td><span class="badge-position badge-position-${result.position <= 3 ? result.position : ''}">${result.position}</span></td>
              <td>${result.driver_name}</td>
              <td>${result.driver_team || 'N/A'}</td>
            </tr>
          `;
        });

        resultsHTML += '</tbody></table></div>';

        alert(resultsHTML); // In a real app, use a proper modal
      }
    } catch (error) {
      console.error('Failed to load results:', error);
      alert('Failed to load race results');
    }
  },

  // Get CSRF token from cookie
  getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  app.init();
});
