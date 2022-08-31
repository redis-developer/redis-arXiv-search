import React, { FC, useState } from 'react';

import { Header } from './views/Header';
import { Home } from './views/Home';
import { Footer } from './views/Footer';


export const Layout: FC = () => {
    const [papers, setPapers] = useState<any[]>([]);
    const [category, setCategory] = useState<string>('');

    return (
        <>
        <Header setPapers={setPapers} papers={papers} category={category} setCategory={setCategory} />
        <Home setPapers={setPapers} papers={papers} category={category} setCategory={setCategory}/>
        <Footer/>
        </>
    );
};

export default Layout;