<script lang="ts">
  let loading = false;
  let resultData: any = null;

  async function formSubmit(e: Event) {
    loading = true;
    const formData = new FormData(e.target as HTMLFormElement);
    const formInput = new URLSearchParams();
    for (let field of formData) {
      const [key, value] = field;
      //@ts-ignore
      formInput.append(key, value);
    }
    if (formInput.get("strategy") === "Select option") {
      alert("please select strategy");
      loading = false;
      return;
    }
    // if(formInput.get('from_date') === "") {
    //     alert("please select from date")
    //     loading = false
    //     return
    // }
    // if(formInput.get('to_date') === "") {
    //     alert("please select to date")
    //     loading = false
    //     return
    // }

    const resp = await fetch(
      `http://127.0.0.1:8000/run_strategy?strategy=${formInput.get("strategy")}&isDay=false&from_date=01/01/2014&to_date=28/05/2024`
    );
    const data = await resp.json();
    resultData = data;
    loading = false;
  }
</script>

<section class="section">
  <div class="container">
    <!-- choose strategy -->

    <form on:submit|preventDefault={(e) => formSubmit(e)}>
      <div class="columns is-multiline">
        <div class="column is-3">
          <div class="field">
            <label class="label">Select Strategy</label>
            <div class="control">
              <div class="select">
                <select name="strategy">
                  <option>Select option</option>
                  <option value="tenandtwentysma">Ten And Twenty SMA</option>
                  <option value="threeandsixema">Three And Six EMA</option>
                  <option value="rsiandmac"
                    >RSI Divergence with MAC Crossover</option
                  >
                  <option value="atrandmaccrossover"
                    >ATR Stop-Loss with MAC Crossover</option
                  >
                  <option value="rsioversoldbounce">RSI Oversold Bounce</option>
                  <option value="breakoutwithvolumeandrsi"
                    >Breakout Confirmation with Volume & RSI Oversold Bounce</option
                  >
                  <option value="volumediscrepancy">Volume Discrepancy</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <div class="column is-3">
          <div class="field">
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label class="label">From Date</label>
            <div class="control">
              <input
                class="input"
                name="from_date"
                type="date"
                value="2014-01-01"
                placeholder="Text input"
              />
            </div>
          </div>
        </div>

        <div class="column is-3">
          <div class="field">
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label class="label">To Date</label>
            <div class="control">
              <input
                class="input"
                name="to_date"
                type="date"
                value="2024-05-28"
                placeholder="Text input"
              />
            </div>
          </div>
        </div>

        <div class="column is-12">
          <div class="field is-grouped">
            <div class="control">
              <button class="button is-link" disabled={loading}>Submit</button>
            </div>
          </div>
        </div>
      </div>
    </form>

    <div class="mt-4">
      {#if loading}
        <!-- content here -->
        <button class="button is-loading-is-large">Data Is Loading</button>
      {:else}
        <!-- else content here -->
        {#if resultData === null}
          <!-- content here -->
          <p>Please select strategy</p>
        {:else}
          <!-- else content here -->
          <table
            class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth"
          >
            <thead>
              <tr>
                <th>Symbol</th>
                <th>From Date</th>
                <th>To Date</th>
                <th>Invest Amount</th>
                <th>Return Amount</th>
                <th>Return Percent</th>
                <th>Standard Deviation</th>
                <th>Beta</th>
                <th>Sharpe Ratio</th>
                <th>Sortino Ratio</th>
                <th>Max Drawdown</th>
                <th>Annualized Return</th>
                <th>View Detail</th>
              </tr>
            </thead>
            <tbody>
              {#each resultData.strategyReturn as item}
                <tr>
                  <td>{item["Symbol"]}</td>
                  <td>{item["From Date"]}</td>
                  <td>{item["To Date"]}</td>
                  <td>{item["Invest Amount"]}</td>
                  <td>{item["Return Amount"]}</td>
                  <td>{item["Return Percent"]}</td>
                  <td>{item["Standard Deviation"]}</td>
                  <td>{item["Beta"]}</td>
                  <td>{item["Sharpe Ratio"]}</td>
                  <td>{item["Sortino Ratio"]}</td>
                  <td>{item["Max Drawdown"]}</td>
                  <td>{item["Annualized Return"]}</td>
                  <th
                    ><a href="/singleStock/{item['Symbol']}">View Detail</a></th
                  >
                </tr>
              {/each}
            </tbody>
          </table>

          <div class="mt-3">
            <p class="title">Monte Carlo Simulation</p>
            <p>Best Case Situation</p>
            <br />
            {@html resultData.bestCaseMS}
            <br />
            <p>Worst Case Situation</p>
            <br />
            {@html resultData.worstCaseMS}
          </div>

          <div class="mt-3">
            <p class="title">Histogram of Monte Carlo Simulation</p>
            <img src="data:image/png;base64,{resultData.histogram}" />'
          </div>

          <div class="mt-3">
            <p class="title">Summary of Monte Carlo Simulation</p>
            <div class="card">
              <div class="card-content">
                {@html resultData.summaryMS}
              </div>
            </div>
          </div>
        {/if}
      {/if}
    </div>
  </div>
</section>
