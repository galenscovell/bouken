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
	<div id=left_container class=center>
		<div class="vertical_sub_container center">
			<div class="vertical_sub_box box-shadow"></div>
			<p class=vertical_sub_text>Placeholder text here</p>
		</div>
		<div class="vertical_sub_container center">
			<div class="vertical_sub_box box-shadow"></div>
			<p class=vertical_sub_text>Placeholder text here</p>
		</div>
		<div class="vertical_sub_container center">
			<div class="vertical_sub_box box-shadow"></div>
			<p class=vertical_sub_text>Placeholder text here</p>
		</div>
		<div class="vertical_sub_container center">
			<div class="vertical_sub_box box-shadow"></div>
			<p class=vertical_sub_text>Placeholder text here</p>
		</div>
	</div>
	
	<div id=right_container class="box-shadow center">
		<div class="vertical_sub_container center">
			<div class="generate_input">
				<label for="pixelWidthLabel">Pixel Width</label>
				<input id="pixelWidthRange" type="range" min="128" max="1280" step="128" value="640" oninput="pixelWidth.value=pixelWidthRange.value" />
				<output id="pixelWidth" for="pixelWidthRange">640</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input">
				<label for="hexSizeLabel">Hex Size</label>
				<input id="hexSizeRange" type="range" min="2" max="16" step="1" value="8" oninput="hexSize.value=hexSizeRange.value" />
				<output id="hexSize" for="hexSizeRange">8</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input">
				<label for="initialLandPctLabel">Initial Land Percentage</label>
				<input id="initialLandPctRange" type="range" min="0" max="100" step="1" value="30" oninput="initialLandPct.value=initialLandPctRange.value" />
				<output id="initialLandPct" for="initialLandPctRange">30</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input">
				<label for="requiredLandPctLabel">Required Land Percentage</label>
				<input id="requiredLandPctRange" type="range" min="0" max="100" step="1" value="40" oninput="requiredLandPct.value=requiredLandPctRange.value" />
				<output id="requiredLandPct" for="requiredLandPctRange">40</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input">
				<label for="terraformIterationsLabel">Terraform Iterations</label>
				<input id="terraformIterationsRange" type="range" min="1" max="32" step="1" value="20" oninput="terraformIterations.value=terraformIterationsRange.value" />
				<output id="terraformIterations" for="terraformIterationsRange">20</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input">
				<label for="minIslandSizeLabel">Minimum Island Hex Size</label>
				<input id="minIslandSizeRange" type="range" min="4" max="32" step="1" value="12" oninput="minIslandSize.value=minIslandSizeRange.value" />
				<output id="minIslandSize" for="minIslandSizeRange">12</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input">
				<label for="temperature">Temperature</label>
				<select name="Temperature">
					<option value="Freezing">Freezing</option>
					<option value="Cold">Cold</option>
					<option value="Temperate">Temperate</option>
					<option value="Warm">Warm</option>
					<option value="Hot">Hot</option>
				</select>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input">
				<label for="humidity">Humidity</label>
				<select id="humidity" name="Humidity">
					<option value="Barren">Barren</option>
					<option value="Dry">Dry</option>
					<option value="Average">Average</option>
					<option value="Wet">Wet</option>
					<option value="Drenched">Drenched</option>
				</select>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input">
				<label for="minRegionExpandsLabel">Minimum Region Expansions</label>
				<input id="minRegionExpandsRange" type="range" min="1" max="6" step="1" value="2" oninput="minRegionExpands.value=minRegionExpandsRange.value" />
				<output id="minRegionExpands" for="minRegionExpandsRange">2</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input">
				<label for="maxRegionExpandsLabel">Maximum Region Expansions</label>
				<input id="maxRegionExpandsRange" type="range" min="1" max="12" step="1" value="5" oninput="maxRegionExpands.value=maxRegionExpandsRange.value" />
				<output id="maxRegionExpands" for="maxRegionExpandsRange">5</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input">
				<label for="minRegionSizePctLabel">Minimum Region Size Percentage</label>
				<input id="minRegionSizePctRange" type="range" min="0" max="5" step="0.25" value="1.25" oninput="minRegionSizePct.value=minRegionSizePctRange.value" />
				<output id="minRegionSizePct" for="minRegionSizePctRange">1.25</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<button class="button box-shadow" on:click="{() => generateExteriorMap()}">Generate</button>
		</div>
	</div>

</div>

<div id=footer_container>

</div>