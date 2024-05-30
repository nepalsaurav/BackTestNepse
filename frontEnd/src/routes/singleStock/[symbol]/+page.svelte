<script lang="ts">
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  let loading = true;
  let singleStockData: any = null;
  const params = $page.params;
  const symbol = params.symbol;
  onMount(async () => {
    const resp = await fetch(
      `http://localhost:8000/single_stock?symbol=${symbol}`
    );
    const resp_text = await resp.json();
    const data = JSON.parse(resp_text);
    singleStockData = data;
    loading = false;
  });
</script>

<section class="section">
  <div class="container">
    {#if loading}
      <p>Data is loading ............</p>
    {:else if singleStockData === null}
      <p>no data found</p>
    {:else}
      <p>Detail Data of {symbol}</p>
      <br />
      <br />

      <table
        class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth"
      >
        <thead>
          <tr>
            <th>Date</th>
            <th>Symbol</th>
            <th>Close</th>
            <th>Invest</th>
            <th>Position</th>
            <th>qtd</th>
          </tr>
        </thead>
        <tbody>
          {#each singleStockData as item}
            <tr>
              <td>{item["Date"]}</td>
              <td>{symbol}</td>
              <td>{item["Close"].toFixed(2)}</td>
              <td>{Number(item["Invest"].toFixed(2)).toLocaleString()}</td>
              <td
                >{item["Position"] === null
                  ? "No any position"
                  : item["Position"]}</td
              >
              <td>{Math.round(item["qtd"])}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </div>
</section>
