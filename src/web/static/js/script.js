document.addEventListener('DOMContentLoaded', function() {
    // Main calculate button
    const calculateButton = document.getElementById('calculateButton');
    const resultsSection = document.getElementById('resultsSection');
    const loadingSection = document.getElementById('loadingSection');
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    
    // Results elements
    const handStrengthBar = document.getElementById('handStrengthBar');
    const handStrengthValue = document.getElementById('handStrengthValue');
    const recommendationValue = document.getElementById('recommendationValue');
    const infoValue = document.getElementById('infoValue');
    
    // Form elements
    const card1Rank = document.getElementById('card1Rank');
    const card1Suit = document.getElementById('card1Suit');
    const card2Rank = document.getElementById('card2Rank');
    const card2Suit = document.getElementById('card2Suit');
    const numPlayers = document.getElementById('numPlayers');
    const position = document.getElementById('position');
    const bigBlinds = document.getElementById('bigBlinds');
    const tournamentStage = document.getElementById('tournamentStage');
    
    // Community card elements
    const useCommunityCards = document.getElementById('useCommunityCards');
    const communityCardsSection = document.getElementById('communityCardsSection');
    const communityCardsContainer = document.getElementById('communityCardsContainer');
    
    // Opponent range elements
    const useOpponentRange = document.getElementById('useOpponentRange');
    const opponentRangeSection = document.getElementById('opponentRangeSection');
    const opponentRange = document.getElementById('opponentRange');
    
    // ICM elements
    const useIcm = document.getElementById('useIcm');
    const icmSection = document.getElementById('icmSection');
    
    // Initialize community cards
    if (communityCardsContainer) {
        // Create 5 community card inputs (flop, turn, river)
        for (let i = 0; i < 5; i++) {
            const cardDiv = document.createElement('div');
            cardDiv.className = 'col-md-2 mb-2';
            
            const cardLabel = document.createElement('label');
            cardLabel.className = 'form-label';
            cardLabel.textContent = i < 3 ? `Flop ${i+1}` : (i === 3 ? 'Turn' : 'River');
            cardDiv.appendChild(cardLabel);
            
            const rankSelect = document.createElement('select');
            rankSelect.className = 'form-select community-rank mb-1';
            rankSelect.innerHTML = `
                <option value="">Rank</option>
                <option value="A">A</option>
                <option value="K">K</option>
                <option value="Q">Q</option>
                <option value="J">J</option>
                <option value="T">T</option>
                <option value="9">9</option>
                <option value="8">8</option>
                <option value="7">7</option>
                <option value="6">6</option>
                <option value="5">5</option>
                <option value="4">4</option>
                <option value="3">3</option>
                <option value="2">2</option>
            `;
            cardDiv.appendChild(rankSelect);
            
            const suitSelect = document.createElement('select');
            suitSelect.className = 'form-select community-suit';
            suitSelect.innerHTML = `
                <option value="">Suit</option>
                <option value="h">♥ Hearts</option>
                <option value="d">♦ Diamonds</option>
                <option value="c">♣ Clubs</option>
                <option value="s">♠ Spades</option>
            `;
            cardDiv.appendChild(suitSelect);
            
            communityCardsContainer.appendChild(cardDiv);
        }
    }
    
    // Toggle community cards section
    if (useCommunityCards) {
        useCommunityCards.addEventListener('change', function() {
            if (this.checked) {
                communityCardsSection.classList.remove('d-none');
            } else {
                communityCardsSection.classList.add('d-none');
            }
        });
    }
    
    // Toggle opponent range section
    if (useOpponentRange) {
        useOpponentRange.addEventListener('change', function() {
            if (this.checked) {
                opponentRangeSection.classList.remove('d-none');
            } else {
                opponentRangeSection.classList.add('d-none');
            }
        });
    }
    
    // Toggle ICM section
    if (useIcm) {
        useIcm.addEventListener('change', function() {
            if (this.checked) {
                icmSection.classList.remove('d-none');
            } else {
                icmSection.classList.add('d-none');
            }
        });
    }
    
    // Update player count display
    if (numPlayers) {
        const numPlayersValue = document.getElementById('numPlayersValue');
        numPlayers.addEventListener('input', function() {
            if (numPlayersValue) {
                numPlayersValue.textContent = `${this.value} players`;
            }
        });
    }
    
    // ICM players slider
    const icmPlayers = document.getElementById('icmPlayers');
    const icmPlayersValue = document.getElementById('icmPlayersValue');
    const icmStacksContainer = document.getElementById('icmStacksContainer');
    
    if (icmPlayers && icmPlayersValue && icmStacksContainer) {
        // Update display and generate stack inputs
        icmPlayers.addEventListener('input', function() {
            const numPlayers = parseInt(this.value);
            icmPlayersValue.textContent = `${numPlayers} players`;
            
            // Generate stack inputs
            icmStacksContainer.innerHTML = '';
            for (let i = 0; i < numPlayers; i++) {
                const colDiv = document.createElement('div');
                colDiv.className = 'col-md-4 mb-2';
                
                const inputGroup = document.createElement('div');
                inputGroup.className = 'input-group';
                
                const inputGroupText = document.createElement('span');
                inputGroupText.className = 'input-group-text';
                inputGroupText.textContent = `P${i+1}`;
                inputGroup.appendChild(inputGroupText);
                
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control';
                input.min = '1';
                input.value = '1000';
                inputGroup.appendChild(input);
                
                colDiv.appendChild(inputGroup);
                icmStacksContainer.appendChild(colDiv);
            }
        });
        
        // Initialize stack inputs
        icmPlayers.dispatchEvent(new Event('input'));
    }
    
    // ICM payouts slider
    const icmPayouts = document.getElementById('icmPayouts');
    const icmPayoutsValue = document.getElementById('icmPayoutsValue');
    const icmPayoutsContainer = document.getElementById('icmPayoutsContainer');
    
    if (icmPayouts && icmPayoutsValue && icmPayoutsContainer) {
        // Update display and generate payout inputs
        icmPayouts.addEventListener('input', function() {
            const numPayouts = parseInt(this.value);
            icmPayoutsValue.textContent = `${numPayouts} payouts`;
            
            // Generate payout inputs
            icmPayoutsContainer.innerHTML = '';
            for (let i = 0; i < numPayouts; i++) {
                const colDiv = document.createElement('div');
                colDiv.className = 'col-md-4 mb-2';
                
                const inputGroup = document.createElement('div');
                inputGroup.className = 'input-group';
                
                const inputGroupText = document.createElement('span');
                inputGroupText.className = 'input-group-text';
                inputGroupText.textContent = `${i+1}${getOrdinalSuffix(i+1)}`;
                inputGroup.appendChild(inputGroupText);
                
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control';
                input.min = '0';
                input.value = (1000 / (i + 1)).toFixed(0); // Simple decreasing payouts
                inputGroup.appendChild(input);
                
                colDiv.appendChild(inputGroup);
                icmPayoutsContainer.appendChild(colDiv);
            }
        });
        
        // Initialize payout inputs
        icmPayouts.dispatchEvent(new Event('input'));
    }
    // ICM Calculator section
    const icmCalcPlayers = document.getElementById('icmCalcPlayers');
    const icmCalcPlayersValue = document.getElementById('icmCalcPlayersValue');
    const icmCalcStacksContainer = document.getElementById('icmCalcStacksContainer');
    
    if (icmCalcPlayers && icmCalcPlayersValue && icmCalcStacksContainer) {
        // Update display and generate stack inputs
        icmCalcPlayers.addEventListener('input', function() {
            const numPlayers = parseInt(this.value);
            icmCalcPlayersValue.textContent = `${numPlayers} players`;
            
            // Generate stack inputs
            icmCalcStacksContainer.innerHTML = '';
            for (let i = 0; i < numPlayers; i++) {
                const colDiv = document.createElement('div');
                colDiv.className = 'col-md-4 mb-2';
                
                const inputGroup = document.createElement('div');
                inputGroup.className = 'input-group';
                
                const inputGroupText = document.createElement('span');
                inputGroupText.className = 'input-group-text';
                inputGroupText.textContent = `P${i+1}`;
                inputGroup.appendChild(inputGroupText);
                
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control';
                input.min = '1';
                input.value = '1000';
                inputGroup.appendChild(input);
                
                colDiv.appendChild(inputGroup);
                icmCalcStacksContainer.appendChild(colDiv);
            }
        });
        
        // Initialize stack inputs
        icmCalcPlayers.dispatchEvent(new Event('input'));
    }
    
    // ICM Calculator payouts slider
    const icmCalcPayouts = document.getElementById('icmCalcPayouts');
    const icmCalcPayoutsValue = document.getElementById('icmCalcPayoutsValue');
    const icmCalcPayoutsContainer = document.getElementById('icmCalcPayoutsContainer');
    
    if (icmCalcPayouts && icmCalcPayoutsValue && icmCalcPayoutsContainer) {
        // Update display and generate payout inputs
        icmCalcPayouts.addEventListener('input', function() {
            const numPayouts = parseInt(this.value);
            icmCalcPayoutsValue.textContent = `${numPayouts} payouts`;
            
            // Generate payout inputs
            icmCalcPayoutsContainer.innerHTML = '';
            for (let i = 0; i < numPayouts; i++) {
                const colDiv = document.createElement('div');
                colDiv.className = 'col-md-4 mb-2';
                
                const inputGroup = document.createElement('div');
                inputGroup.className = 'input-group';
                
                const inputGroupText = document.createElement('span');
                inputGroupText.className = 'input-group-text';
                inputGroupText.textContent = `${i+1}${getOrdinalSuffix(i+1)}`;
                inputGroup.appendChild(inputGroupText);
                
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control';
                input.min = '0';
                input.value = (1000 / (i + 1)).toFixed(0); // Simple decreasing payouts
                inputGroup.appendChild(input);
                
                colDiv.appendChild(inputGroup);
                icmCalcPayoutsContainer.appendChild(colDiv);
            }
        });
        
        // Initialize payout inputs
        icmCalcPayouts.dispatchEvent(new Event('input'));
    }
    
    // Nash Ranges section
    const nashPlayers = document.getElementById('nashPlayers');
    const nashPlayersValue = document.getElementById('nashPlayersValue');
    const nashPositionsContainer = document.getElementById('nashPositionsContainer');
    const nashStacksContainer = document.getElementById('nashStacksContainer');
    
    if (nashPlayers && nashPlayersValue && nashPositionsContainer && nashStacksContainer) {
        // Update display and generate position/stack inputs
        nashPlayers.addEventListener('input', function() {
            const numPlayers = parseInt(this.value);
            nashPlayersValue.textContent = `${numPlayers} players`;
            
            // Generate position inputs
            nashPositionsContainer.innerHTML = '';
            for (let i = 0; i < numPlayers; i++) {
                const colDiv = document.createElement('div');
                colDiv.className = 'col-md-4 mb-2';
                
                const label = document.createElement('label');
                label.className = 'form-label';
                label.textContent = `Player ${i+1} Position`;
                colDiv.appendChild(label);
                
                const select = document.createElement('select');
                select.className = 'form-select';
                
                // Add position options
                const positions = ['BTN', 'SB', 'BB', 'UTG', 'MP', 'CO'];
                for (const pos of positions) {
                    const option = document.createElement('option');
                    option.value = pos;
                    option.textContent = pos;
                    select.appendChild(option);
                }
                
                // Set default position based on index
                select.value = positions[i % positions.length];
                
                colDiv.appendChild(select);
                nashPositionsContainer.appendChild(colDiv);
            }
            
            // Generate stack inputs
            nashStacksContainer.innerHTML = '';
            for (let i = 0; i < numPlayers; i++) {
                const colDiv = document.createElement('div');
                colDiv.className = 'col-md-4 mb-2';
                
                const inputGroup = document.createElement('div');
                inputGroup.className = 'input-group';
                
                const inputGroupText = document.createElement('span');
                inputGroupText.className = 'input-group-text';
                inputGroupText.textContent = `P${i+1}`;
                inputGroup.appendChild(inputGroupText);
                
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control';
                input.min = '1';
                input.value = i === 0 ? '15' : '20'; // First player has smaller stack
                inputGroup.appendChild(input);
                
                colDiv.appendChild(inputGroup);
                nashStacksContainer.appendChild(colDiv);
            }
        });
        
        // Initialize inputs
        nashPlayers.dispatchEvent(new Event('input'));
    }
    
    // Nash payouts slider
    const nashPayouts = document.getElementById('nashPayouts');
    const nashPayoutsValue = document.getElementById('nashPayoutsValue');
    const nashPayoutsContainer = document.getElementById('nashPayoutsContainer');
    const useIcmNash = document.getElementById('useIcmNash');
    const nashIcmSection = document.getElementById('nashIcmSection');
    
    if (useIcmNash && nashIcmSection) {
        useIcmNash.addEventListener('change', function() {
            if (this.checked) {
                nashIcmSection.classList.remove('d-none');
            } else {
                nashIcmSection.classList.add('d-none');
            }
        });
    }
    
    if (nashPayouts && nashPayoutsValue && nashPayoutsContainer) {
        // Update display and generate payout inputs
        nashPayouts.addEventListener('input', function() {
            const numPayouts = parseInt(this.value);
            nashPayoutsValue.textContent = `${numPayouts} payouts`;
            
            // Generate payout inputs
            nashPayoutsContainer.innerHTML = '';
            for (let i = 0; i < numPayouts; i++) {
                const colDiv = document.createElement('div');
                colDiv.className = 'col-md-4 mb-2';
                
                const inputGroup = document.createElement('div');
                inputGroup.className = 'input-group';
                
                const inputGroupText = document.createElement('span');
                inputGroupText.className = 'input-group-text';
                inputGroupText.textContent = `${i+1}${getOrdinalSuffix(i+1)}`;
                inputGroup.appendChild(inputGroupText);
                
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control';
                input.min = '0';
                input.value = (1000 / (i + 1)).toFixed(0); // Simple decreasing payouts
                inputGroup.appendChild(input);
                
                colDiv.appendChild(inputGroup);
                nashPayoutsContainer.appendChild(colDiv);
            }
        });
        
        // Initialize payout inputs
        nashPayouts.dispatchEvent(new Event('input'));
    }
    
    // Helper function for ordinal suffixes
    function getOrdinalSuffix(num) {
        const j = num % 10;
        const k = num % 100;
        if (j === 1 && k !== 11) {
            return "st";
        }
        if (j === 2 && k !== 12) {
            return "nd";
        }
        if (j === 3 && k !== 13) {
            return "rd";
        }
        return "th";
    }
    // Main calculate button handler
    if (calculateButton) {
        calculateButton.addEventListener('click', function() {
            // Hide previous results and errors
            if (resultsSection) resultsSection.classList.add('d-none');
            if (errorSection) errorSection.classList.add('d-none');
            
            // Show loading indicator
            if (loadingSection) loadingSection.classList.remove('d-none');
            
            // Validate hole cards
            if (!card1Rank.value || !card1Suit.value || !card2Rank.value || !card2Suit.value) {
                showError('Please select both hole cards completely.');
                return;
            }
            
            // Prepare data for API call
            const data = {
                numPlayers: parseInt(numPlayers.value),
                card1: card1Rank.value + card1Suit.value,
                card2: card2Rank.value + card2Suit.value,
                position: position.value,
                tournamentStage: tournamentStage.value
            };
            
            // Add big blinds if provided
            if (bigBlinds && bigBlinds.value) {
                const bbValue = parseInt(bigBlinds.value);
                if (isNaN(bbValue) || bbValue <= 0) {
                    showError('Big blinds must be a positive number');
                    return;
                }
                data.bigBlinds = bbValue;
            }
            
            // Add community cards if enabled
            if (useCommunityCards && useCommunityCards.checked) {
                const communityRanks = document.querySelectorAll('.community-rank');
                const communitySuits = document.querySelectorAll('.community-suit');
                const communityCards = [];
                
                for (let i = 0; i < communityRanks.length; i++) {
                    const rank = communityRanks[i].value;
                    const suit = communitySuits[i].value;
                    
                    if (rank && suit) {
                        communityCards.push(rank + suit);
                    } else if (rank || suit) {
                        showError(`Community card ${i+1} is incomplete. Please select both rank and suit.`);
                        return;
                    }
                }
                
                // Validate community cards sequence
                if (communityCards.length > 0) {
                    // First 3 should be flop
                    if (communityCards.length >= 1 && communityCards.length < 3) {
                        if (communityCards[0] && (!communityCards[1] || !communityCards[2])) {
                            showError('If any flop card is specified, all 3 flop cards must be specified.');
                            return;
                        }
                    }
                    
                    // If turn is specified (index 3), all flop cards must be specified
                    if (communityCards.length >= 4 && (!communityCards[0] || !communityCards[1] || !communityCards[2])) {
                        showError('If turn is specified, all flop cards must be specified.');
                        return;
                    }
                    
                    // If river is specified (index 4), turn and all flop cards must be specified
                    if (communityCards.length === 5 && !communityCards[3]) {
                        showError('If river is specified, turn and all flop cards must be specified.');
                        return;
                    }
                }
                
                data.communityCards = communityCards;
            }
            
            // Add opponent range if enabled
            if (useOpponentRange && useOpponentRange.checked && opponentRange && opponentRange.value) {
                data.opponentRange = opponentRange.value;
            }
            
            // Add ICM data if enabled
            if (useIcm && useIcm.checked) {
                const stackInputs = document.querySelectorAll('#icmStacksContainer input');
                const stackSizes = [];
                for (const input of stackInputs) {
                    const value = parseInt(input.value);
                    if (isNaN(value) || value <= 0) {
                        showError('All stack sizes must be positive numbers');
                        return;
                    }
                    stackSizes.push(value);
                }
                
                const payoutInputs = document.querySelectorAll('#icmPayoutsContainer input');
                const payouts = [];
                for (const input of payoutInputs) {
                    const value = parseInt(input.value);
                    if (isNaN(value) || value < 0) {
                        showError('All payouts must be non-negative numbers');
                        return;
                    }
                    payouts.push(value);
                }
                
                data.icmData = {
                    stackSizes: stackSizes,
                    payouts: payouts,
                    playerIndex: 0 // Assume the user is player 1
                };
            }
            
            console.log("Sending data:", data);
            
            // Make API call
            fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || 'An error occurred during calculation.');
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log("Received response:", data);
                
                // Hide loading indicator
                if (loadingSection) loadingSection.classList.add('d-none');
                
                // Update results
                if (handStrengthBar) handStrengthBar.style.width = `${data.handStrength}%`;
                if (handStrengthValue) handStrengthValue.textContent = `${data.handStrength}%`;
                
                if (recommendationValue) {
                    recommendationValue.textContent = data.recommendation;
                    
                    // Set color based on recommendation
                    if (data.recommendation === "Fold") {
                        recommendationValue.style.color = "#e74c3c"; // Red
                    } else if (data.recommendation === "Call") {
                        recommendationValue.style.color = "#f39c12"; // Orange
                    } else {
                        recommendationValue.style.color = "#27ae60"; // Green
                    }
                }
                
                if (infoValue) infoValue.textContent = data.info;
                
                // Show results section
                if (resultsSection) resultsSection.classList.remove('d-none');
                
                // Scroll to results
                if (resultsSection) resultsSection.scrollIntoView({ behavior: 'smooth' });
            })
            .catch(error => {
                console.error("Error:", error);
                showError(error.message);
            });
        });
    }
    
    // Helper function to show error message
    function showError(message) {
        if (loadingSection) loadingSection.classList.add('d-none');
        if (errorMessage) errorMessage.textContent = message;
        if (errorSection) errorSection.classList.remove('d-none');
        console.error("Error:", message);
    }
    
    // ICM Calculator button
    const calculateIcmButton = document.getElementById('calculateIcmButton');
    const icmResultsSection = document.getElementById('icmResultsSection');
    const icmLoadingSection = document.getElementById('icmLoadingSection');
    const icmErrorSection = document.getElementById('icmErrorSection');
    const icmErrorMessage = document.getElementById('icmErrorMessage');
    const icmResultsTable = document.getElementById('icmResultsTable');
    const icmImplications = document.getElementById('icmImplications');
    
    if (calculateIcmButton) {
        calculateIcmButton.addEventListener('click', function() {
            // Hide previous results and errors
            if (icmResultsSection) icmResultsSection.classList.add('d-none');
            if (icmErrorSection) icmErrorSection.classList.add('d-none');
            
            // Show loading indicator
            if (icmLoadingSection) icmLoadingSection.classList.remove('d-none');
            
            // Get stack sizes
            const stackInputs = document.querySelectorAll('#icmCalcStacksContainer input');
            const stackSizes = [];
            for (const input of stackInputs) {
                const value = parseInt(input.value);
                if (isNaN(value) || value <= 0) {
                    showIcmError('All stack sizes must be positive numbers');
                    return;
                }
                stackSizes.push(value);
            }
            
            if (stackSizes.length === 0) {
                showIcmError('Please add at least one stack size');
                return;
            }
            
            // Get payouts
            const payoutInputs = document.querySelectorAll('#icmCalcPayoutsContainer input');
            const payouts = [];
            for (const input of payoutInputs) {
                const value = parseInt(input.value);
                if (isNaN(value) || value < 0) {
                    showIcmError('All payouts must be non-negative numbers');
                    return;
                }
                payouts.push(value);
            }
            
            if (payouts.length === 0) {
                showIcmError('Please add at least one payout');
                return;
            }
            
            // Prepare data for API call
            const data = {
                stackSizes: stackSizes,
                payouts: payouts
            };
            
            console.log("Sending ICM data:", data);
            
            // Make API call
            fetch('/calculate_icm', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || 'An error occurred during ICM calculation.');
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log("Received ICM response:", data);
                
                // Hide loading indicator
                if (icmLoadingSection) icmLoadingSection.classList.add('d-none');
                
                // Update results table
                if (icmResultsTable) {
                    icmResultsTable.innerHTML = '';
                    
                    const totalStack = stackSizes.reduce((a, b) => a + b, 0);
                    
                    for (let i = 0; i < stackSizes.length; i++) {
                        const row = document.createElement('tr');
                        
                        // Player column
                        const playerCell = document.createElement('td');
                        playerCell.textContent = `Player ${i + 1}`;
                        row.appendChild(playerCell);
                        
                        // Stack column
                        const stackCell = document.createElement('td');
                        stackCell.textContent = stackSizes[i];
                        row.appendChild(stackCell);
                        
                        // Stack % column
                        const stackPctCell = document.createElement('td');
                        const stackPct = (stackSizes[i] / totalStack * 100).toFixed(2);
                        stackPctCell.textContent = `${stackPct}%`;
                        row.appendChild(stackPctCell);
                        
                        // ICM Value column
                        const icmValueCell = document.createElement('td');
                        icmValueCell.textContent = data.icmValues[i].toFixed(2);
                        row.appendChild(icmValueCell);
                        
                        // ICM % column
                        const icmPctCell = document.createElement('td');
                        const totalPayout = payouts.reduce((a, b) => a + b, 0);
                        const icmPct = (data.icmValues[i] / totalPayout * 100).toFixed(2);
                        icmPctCell.textContent = `${icmPct}%`;
                        row.appendChild(icmPctCell);
                        
                        // ICM Pressure column
                        const pressureCell = document.createElement('td');
                        pressureCell.textContent = `${data.icmPressures[i]}%`;
                        
                        // Color code pressure
                        if (data.icmPressures[i] > 70) {
                            pressureCell.style.color = "#e74c3c"; // Red for high pressure
                        } else if (data.icmPressures[i] > 40) {
                            pressureCell.style.color = "#f39c12"; // Orange for medium pressure
                        } else {
                            pressureCell.style.color = "#27ae60"; // Green for low pressure
                        }
                        
                        row.appendChild(pressureCell);
                        
                        icmResultsTable.appendChild(row);
                    }
                }
                
                // Update implications
                if (icmImplications) {
                    icmImplications.innerHTML = '';
                    
                    // Add some general implications
                    const implications = [
                        "Players with high ICM pressure should play more conservatively",
                        "Short stacks should focus on survival when close to pay jumps",
                        "Big stacks can put pressure on medium stacks near the bubble"
                    ];
                    
                    for (const implication of implications) {
                        const li = document.createElement('li');
                        li.textContent = implication;
                        icmImplications.appendChild(li);
                    }
                    
                    // Add specific implications based on results
                    const highestPressureIndex = data.icmPressures.indexOf(Math.max(...data.icmPressures));
                    if (highestPressureIndex >= 0) {
                        const li = document.createElement('li');
                        li.textContent = `Player ${highestPressureIndex + 1} has the highest ICM pressure and should be most cautious`;
                        icmImplications.appendChild(li);
                    }
                }
                
                // Show results section
                if (icmResultsSection) icmResultsSection.classList.remove('d-none');
                
                // Scroll to results
                if (icmResultsSection) icmResultsSection.scrollIntoView({ behavior: 'smooth' });
            })
            .catch(error => {
                console.error("ICM Error:", error);
                showIcmError(error.message);
            });
        });
    }
    
    // Helper function to show ICM error message
    function showIcmError(message) {
        if (icmLoadingSection) icmLoadingSection.classList.add('d-none');
        if (icmErrorMessage) icmErrorMessage.textContent = message;
        if (icmErrorSection) icmErrorSection.classList.remove('d-none');
        console.error("ICM Error:", message);
    }
    // Nash Ranges button
    const calculateNashButton = document.getElementById('calculateNashButton');
    const nashResultsSection = document.getElementById('nashResultsSection');
    const nashLoadingSection = document.getElementById('nashLoadingSection');
    const nashErrorSection = document.getElementById('nashErrorSection');
    const nashErrorMessage = document.getElementById('nashErrorMessage');
    const nashResultsContainer = document.getElementById('nashResultsContainer');
    
    if (calculateNashButton) {
        calculateNashButton.addEventListener('click', function() {
            // Hide previous results and errors
            if (nashResultsSection) nashResultsSection.classList.add('d-none');
            if (nashErrorSection) nashErrorSection.classList.add('d-none');
            
            // Show loading indicator
            if (nashLoadingSection) nashLoadingSection.classList.remove('d-none');
            
            // Get positions
            const positionInputs = document.querySelectorAll('#nashPositionsContainer select');
            const positions = [];
            for (const input of positionInputs) {
                positions.push(input.value);
            }
            
            if (positions.length === 0) {
                showNashError('Please add at least one position');
                return;
            }
            
            // Get stack sizes
            const stackInputs = document.querySelectorAll('#nashStacksContainer input');
            const stackSizes = [];
            for (const input of stackInputs) {
                const value = parseInt(input.value);
                if (isNaN(value) || value <= 0) {
                    showNashError('All stack sizes must be positive numbers');
                    return;
                }
                stackSizes.push(value);
            }
            
            if (stackSizes.length === 0) {
                showNashError('Please add at least one stack size');
                return;
            }
            
            // Get blinds
            const sbInput = document.getElementById('nashSb');
            const bbInput = document.getElementById('nashBb');
            
            if (!sbInput || !bbInput) {
                showNashError('Blind inputs not found');
                return;
            }
            
            const sb = parseFloat(sbInput.value);
            const bb = parseFloat(bbInput.value);
            
            if (isNaN(sb) || sb <= 0 || isNaN(bb) || bb <= 0) {
                showNashError('Blinds must be positive numbers');
                return;
            }
            
            // Get payouts if ICM is enabled
            let payouts = null;
            const useIcmNash = document.getElementById('useIcmNash');
            
            if (useIcmNash && useIcmNash.checked) {
                const payoutInputs = document.querySelectorAll('#nashPayoutsContainer input');
                payouts = [];
                for (const input of payoutInputs) {
                    const value = parseInt(input.value);
                    if (isNaN(value) || value < 0) {
                        showNashError('All payouts must be non-negative numbers');
                        return;
                    }
                    payouts.push(value);
                }
                
                if (payouts.length === 0) {
                    showNashError('Please add at least one payout');
                    return;
                }
            }
            
            // Prepare data for API call
            const data = {
                stackSizes: stackSizes,
                positions: positions,
                blinds: [sb, bb]
            };
            
            if (payouts) {
                data.payouts = payouts;
            }
            
            console.log("Sending Nash data:", data);
            
            // Make API call
            fetch('/nash_ranges', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || 'An error occurred during Nash ranges calculation.');
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log("Received Nash response:", data);
                
                // Hide loading indicator
                if (nashLoadingSection) nashLoadingSection.classList.add('d-none');
                
                // Update results
                if (nashResultsContainer) {
                    nashResultsContainer.innerHTML = '';
                    
                    const nashRanges = data.nashRanges;
                    
                    for (const position in nashRanges) {
                        const card = document.createElement('div');
                        card.className = 'card mb-3';
                        
                        const cardHeader = document.createElement('div');
                        cardHeader.className = 'card-header bg-warning text-dark';
                        cardHeader.innerHTML = `<h4>${position} Position</h4>`;
                        card.appendChild(cardHeader);
                        
                        const cardBody = document.createElement('div');
                        cardBody.className = 'card-body';
                        
                        const rangeTitle = document.createElement('h5');
                        rangeTitle.textContent = 'Push Range:';
                        cardBody.appendChild(rangeTitle);
                        
                        const rangeParagraph = document.createElement('p');
                        rangeParagraph.className = 'lead';
                        rangeParagraph.textContent = nashRanges[position].join(', ');
                        cardBody.appendChild(rangeParagraph);
                        
                        card.appendChild(cardBody);
                        nashResultsContainer.appendChild(card);
                    }
                }
                
                // Show results section
                if (nashResultsSection) nashResultsSection.classList.remove('d-none');
                
                // Scroll to results
                if (nashResultsSection) nashResultsSection.scrollIntoView({ behavior: 'smooth' });
            })
            .catch(error => {
                console.error("Nash Error:", error);
                showNashError(error.message);
            });
        });
    }
    
    // Helper function to show Nash error message
    function showNashError(message) {
        if (nashLoadingSection) nashLoadingSection.classList.add('d-none');
        if (nashErrorMessage) nashErrorMessage.textContent = message;
        if (nashErrorSection) nashErrorSection.classList.remove('d-none');
        console.error("Nash Error:", message);
    }
});
