import { NavLink, Outlet } from 'react-router';
import classes from './layout.module.css';

import { ThemeSelector } from './ThemeSelector';
import { GiHelp } from "react-icons/gi";
import Footer from './Footer'
function Layout() {
	



	return (
		<>
			<div className={classes.wrapper}>
				<header className={classes.header}>
					<div className="container">
						<NavLink to="/" className={classes.brand}>
							<svg className={classes.logo} height="800px" width="800px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 471.701 471.701">
								<g>
									<path d="M 235.701 410.701 L 57.401 232.401 C 37.801 212.801 27.001 186.801 27.001 159.101 C 27.001 131.401 37.701 105.401 57.301 85.901 C 76.801 66.401 102.801 55.601 130.401 55.601 C 158.101 55.601 184.201 66.401 203.801 86.001 L 226.401 108.601 C 231.701 113.901 240.201 113.901 245.501 108.601 L 267.901 86.201 C 287.501 66.601 313.601 55.801 341.201 55.801 C 368.801 55.801 394.801 66.601 414.401 86.101 C 434.001 105.701 444.701 131.701 444.701 159.401 C 445.143 169.793 456.67 175.81 465.449 170.231 C 469.178 167.86 471.513 163.816 471.701 159.401 C 471.801 124.501 458.301 91.701 433.601 67.001 C 408.901 42.301 376.201 28.801 341.301 28.801 C 306.401 28.801 273.601 42.401 248.901 67.101 L 236.001 80.001 L 222.901 66.901 C 198.201 42.201 165.301 28.501 130.401 28.501 C 95.601 28.501 62.801 42.101 38.201 66.701 C 13.501 91.401 -0.099 124.201 0.001 159.101 C 0.001 194.001 13.701 226.701 38.401 251.401 L 226.201 439.201 C 228.801 441.801 232.301 443.201 235.701 443.201 M 235.701 443.201 L 235.701 410.701" />
								</g>
								<g transform="matrix(0.302612, 0, 0, 0.302612, 195.661041, 148.475906)">
									<path d="M248.709,421.475c28.995,0,52.5-23.505,52.5-52.5s-23.505-52.5-52.5-52.5h-58.165 c20.598-38.935,49.764-73.439,85.14-100.095c52.277-39.393,114.623-60.214,180.296-60.214c34.612,0,68.514,5.831,100.764,17.331 c31.17,11.115,60.16,27.273,86.16,48.024c52.043,41.536,89.225,99.817,104.695,164.109c5.789,24.063,27.293,40.231,51,40.229 c4.062,0,8.199-0.477,12.324-1.469c28.189-6.783,45.545-35.135,38.762-63.325c-10.559-43.872-28.305-85.42-52.748-123.492 c-23.996-37.372-53.783-70.384-88.535-98.119c-35.098-28.012-74.258-49.833-116.393-64.858 c-43.6-15.547-89.367-23.431-136.03-23.431c-44.688,0-88.618,7.244-130.576,21.529c-40.568,13.813-78.557,33.942-112.908,59.827 c-33.947,25.58-63.55,56.175-87.985,90.936c-6.982,9.932-13.478,20.147-19.511,30.605v-83.971c0-28.995-23.505-52.5-52.5-52.5 S0,141.097,0,170.092v198.884c0,28.995,23.505,52.5,52.5,52.5L248.709,421.475L248.709,421.475z" />
									<path d="M859.691,490.717H663.48c-28.994,0-52.5,23.506-52.5,52.5c0,28.996,23.506,52.5,52.5,52.5h58.027 c-23.443,44.539-57.707,82.494-100.008,110.547c-49.053,32.531-106.244,49.738-165.397,49.762 c-34.575-0.012-68.441-5.842-100.657-17.33c-31.172-11.115-60.16-27.273-86.161-48.025 c-52.044-41.535-89.225-99.816-104.694-164.107c-6.782-28.189-35.132-45.543-63.325-38.762 c-28.19,6.783-45.544,35.135-38.761,63.324c10.556,43.873,28.303,85.422,52.748,123.492c23.995,37.373,53.782,70.385,88.534,98.119 c35.098,28.014,74.258,49.834,116.393,64.859c43.477,15.502,89.107,23.381,135.634,23.426c0.056,0,0.109,0.004,0.166,0.004 c0.042,0,0.083,0,0.125,0c0.036,0,0.07,0,0.106,0c0.043,0,0.086-0.002,0.13-0.002c79.779-0.07,156.951-23.322,223.195-67.256 c52.834-35.039,96.381-81.557,127.656-135.996v84.33c0,28.994,23.504,52.5,52.5,52.5c28.994,0,52.5-23.506,52.5-52.5V543.217 C912.191,514.223,888.686,490.717,859.691,490.717z" />
								</g>
							</svg>
							Senior Sync
						</NavLink>
						<div className={classes.themeSelector}>
							<ThemeSelector />
						</div>
						<NavLink to="/UserGuide" className={classes.helpIcon}><GiHelp  title='Press for help'/></NavLink>
					</div>
				</header>
				<main>
					<div className='container'>
						<Outlet />
					</div>
				</main>
			</div>
				<footer>
					<div className={classes.footer}>
					<Footer /> 
					</div>
					
				</footer>
				
			
			
			
		</>
	);
}

export default Layout;