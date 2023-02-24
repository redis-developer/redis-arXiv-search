import { FC } from 'react';
import { Header } from './views/Header';
import { Home } from './views/Home';
import { Footer } from './views/Footer';

export const Layout: FC = () => {
    return (
        <>
        <Header/>
        <Home/>
        <Footer/>
        </>
    );
};

export default Layout;