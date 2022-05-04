<script lang="ts">
	import { onMount } from 'svelte';
	import axios, { type AxiosResponse } from 'axios';
	import { Humidity, Temperature } from './enums';

	let exteriorMapData: string;
	let exteriorGenerationError: unknown = null;
	let exteriorGenerationRequest = JSON.stringify({
		'pixel_width': 900,
		'hex_size': 10,
		'initial_land_pct': 0.3,
		'required_land_pct': 0.4,
		'terraform_iterations': 20,
		'min_island_size': 12,
		'humidity': Humidity.Average,
		'temperature': Temperature.Temperate,
		'min_region_expansions': 2,
		'max_region_expansions': 5,
		'min_region_size_pct': 0.0125
	})

	async function generateExteriorMap() {
		await axios.post('http://localhost:5050/generate/exterior',
			exteriorGenerationRequest, {
				headers: {'Content-Type': 'application/json'},
				params: {}
		})
		.then(function (response: AxiosResponse) {
			console.log(response);
			exteriorMapData = response.data.map_str
		})
		.catch(function (error) {
			console.log(error);
			exteriorGenerationError = error
		});
	}
</script>

<div id=header_container>

</div>

<div id=root_container>
	<div id=left_root_container>
		<div id=about_site_container>
			<div class=vertical_sub_box></div>
			<div class=vertical_sub_box></div>
			<div class=vertical_sub_box></div>
			<div class=vertical_sub_box></div>
		</div>
	</div>
	
	<div id=right_root_container>
		<div id=generate_container>
			<button on:click="{() => generateExteriorMap()}">Generate Exterior</button>
			<div>
				{#if exteriorMapData}
					<p>{exteriorMapData}</p>
				{:else if exteriorGenerationError}
					<p>Error encountered: {exteriorGenerationError}</p>
				{:else}
					<p>Waiting to hit API...</p>
				{/if}
			</div>
		</div>
	</div>

</div>

<div id=footer_container>

</div>