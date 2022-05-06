<script lang="ts">
	import axios, { type AxiosResponse } from 'axios';
	import { Humidity, Temperature } from './enums';

	let pixelWidth: number = 640;
	let hexSize: number = 8;
	let initialLandPct: number = 30;
	let requiredLandPct: number = 40;
	let terraformIterations: number = 20;
	let minIslandSize: number = 12;
	let humidity: string = "Barren";
	let temperature: string = "Freezing";
	let minRegionExpands: number = 2;
	let maxRegionExpands: number = 5;
	let minRegionSizePct: number = 1.25;

	async function generateExteriorMap() {
		let exteriorMapData: string;
		let exteriorGenerationError: unknown = null;
		let exteriorGenerationRequest = {
			'pixel_width': pixelWidth,
			'hex_size': hexSize,
			'initial_land_pct': initialLandPct / 100,
			'required_land_pct': requiredLandPct / 100,
			'terraform_iterations':terraformIterations,
			'min_island_size': minIslandSize,
			'humidity': Humidity[humidity as keyof typeof Humidity],
			'temperature': Temperature[temperature as keyof typeof Temperature],
			'min_region_expansions': minRegionExpands,
			'max_region_expansions': maxRegionExpands,
			'min_region_size_pct': minRegionSizePct / 100
		};

		console.log(exteriorGenerationRequest);
		await axios.post('http://localhost:5050/generate/exterior',
			JSON.stringify(exteriorGenerationRequest), {
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
			<div class="generate_input box-shadow">
				<label for="pixelWidthLabel">Pixel Width</label>
				<input bind:value={pixelWidth} id="pixelWidthRange" type="range" min="128" max="1280" step="128" oninput="pixelWidth.value=pixelWidthRange.value" />
				<output id="pixelWidth" for="pixelWidthRange">640</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input box-shadow">
				<label for="hexSizeLabel">Hex Size</label>
				<input bind:value={hexSize} id="hexSizeRange" type="range" min="2" max="16" step="1" oninput="hexSize.value=hexSizeRange.value" />
				<output id="hexSize" for="hexSizeRange">8</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input box-shadow">
				<label for="initialLandPctLabel">Initial Land Percentage</label>
				<input bind:value={initialLandPct} id="initialLandPctRange" type="range" min="0" max="90" step="1" oninput="initialLandPct.value=initialLandPctRange.value" />
				<output id="initialLandPct" for="initialLandPctRange">30</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input box-shadow">
				<label for="requiredLandPctLabel">Required Land Percentage</label>
				<input bind:value={requiredLandPct} id="requiredLandPctRange" type="range" min="0" max="90" step="1" oninput="requiredLandPct.value=requiredLandPctRange.value" />
				<output id="requiredLandPct" for="requiredLandPctRange">40</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input box-shadow">
				<label for="terraformIterationsLabel">Terraform Iterations</label>
				<input bind:value={terraformIterations} id="terraformIterationsRange" type="range" min="1" max="32" step="1" oninput="terraformIterations.value=terraformIterationsRange.value" />
				<output id="terraformIterations" for="terraformIterationsRange">20</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input box-shadow">
				<label for="minIslandSizeLabel">Minimum Island Hex Size</label>
				<input bind:value={minIslandSize} id="minIslandSizeRange" type="range" min="4" max="32" step="1" oninput="minIslandSize.value=minIslandSizeRange.value" />
				<output id="minIslandSize" for="minIslandSizeRange">12</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input box-shadow">
				<label for="humidity">Humidity</label>
				<select bind:value={humidity} id="humidity" name="Humidity">
					<option value="Barren">Barren</option>
					<option value="Dry">Dry</option>
					<option value="Average">Average</option>
					<option value="Wet">Wet</option>
					<option value="Drenched">Drenched</option>
				</select>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input box-shadow">
				<label for="temperature">Temperature</label>
				<select bind:value={temperature} name="Temperature">
					<option value="Freezing">Freezing</option>
					<option value="Cold">Cold</option>
					<option value="Temperate">Temperate</option>
					<option value="Warm">Warm</option>
					<option value="Hot">Hot</option>
				</select>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input box-shadow">
				<label for="minRegionExpandsLabel">Minimum Region Expansions</label>
				<input bind:value={minRegionExpands} id="minRegionExpandsRange" type="range" min="1" max="5" step="1" oninput="minRegionExpands.value=minRegionExpandsRange.value" />
				<output id="minRegionExpands" for="minRegionExpandsRange">2</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input box-shadow">
				<label for="maxRegionExpandsLabel">Maximum Region Expansions</label>
				<input bind:value={maxRegionExpands} id="maxRegionExpandsRange" type="range" min="1" max="10" step="1" oninput="maxRegionExpands.value=maxRegionExpandsRange.value" />
				<output id="maxRegionExpands" for="maxRegionExpandsRange">5</output>
			</div>
		</div>
		<div class="vertical_sub_container center">
			<div class="generate_input box-shadow">
				<label for="minRegionSizePctLabel">Minimum Region Size Percentage</label>
				<input bind:value={minRegionSizePct} id="minRegionSizePctRange" type="range" min="0" max="6" step="0.25" oninput="minRegionSizePct.value=minRegionSizePctRange.value" />
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