<script lang="ts">
	import { onMount } from 'svelte';
	import axios, { type AxiosResponse } from 'axios';

	let response: string;
	let error: unknown = null;

	async function generateExteriorMap() {
		try {
			const res: AxiosResponse = await axios.post('http://localhost:5050/generate',{
				headers: {},
				params: {}
			});
			response = res.data.map_str
		} catch (e: unknown) {
			error = e
		}
	}
</script>

<h1>Bouken Map Generator</h1>
<button on:click="{() => generateExteriorMap()}">Generate Exterior</button>
<div>
	{#if response}
		<p>{response}</p>
	{:else if error}
		<p>Error encountered: {error}</p>
	{:else}
		<p>Waiting to hit API...</p>
	{/if}
</div>