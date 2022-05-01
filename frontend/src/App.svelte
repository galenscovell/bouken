<script lang="ts">
	import { onMount } from 'svelte';
	import axios, { type AxiosResponse } from 'axios';

	let response: string;
	let name: string = 'world';
	let error: unknown = null;

	onMount(async () => {
		try {
			const res: AxiosResponse = await axios.get('http://localhost:5050/status',{
				headers: {

				},
				params: {}
			});
			response = res.data.status
		} catch (e: unknown) {
			error = e
		}
	});
</script>

<h1>Hello {name}!</h1>
<div>
	{#if response}
		<p>API Status: {response}</p>
	{:else}
		<p>Hitting API...</p>
	{/if}
</div>