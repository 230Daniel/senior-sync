import { useState } from 'react';
import { NavLink, Outlet } from 'react-router';
import { IoClose, IoMenu } from 'react-icons/io5';

import classes from './layout.module.css';


function Layout() {
	const [showMenu, setShowMenu] = useState(false);

	return (
		<>
			<header>
				<nav className={classes.navbar}>
					<NavLink to="/" className={classes.logo}>
						Senior Sync
					</NavLink>
					<div className={`${classes.menu} ${showMenu ? '' : classes.menuHidden}`}>

					</div>
					<ul className={classes.list}>
						<li className={classes.item}>
							<NavLink to="/news" className={classes.link}>
								News
							</NavLink>
						</li>
						<li className={classes.item}>
							<NavLink to="/about-us" className={classes.link}>
								About Us
							</NavLink>
						</li>
					</ul>
					<div className={classes.close} id="nav-close">
						<IoClose />
					</div>
					<div className={classes.toggle} id="nav-toggle">
						<IoMenu />
					</div>
				</nav>
			</header>
			<main>
				<Outlet />
			</main>
		</>
	);
}

export default Layout;
