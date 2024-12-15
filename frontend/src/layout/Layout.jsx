import { NavLink, Outlet } from 'react-router';

import classes from './layout.module.css';

function Layout() {
	return (
		<>
			<header className={classes.header}>
				<NavLink to="/" className={classes.brand}>
					<img className={classes.logo} src="/seniorsync.svg" />
					Senior Sync
				</NavLink>
			</header>
			<main>
				<Outlet />
			</main>
		</>
	);
}

export default Layout;
