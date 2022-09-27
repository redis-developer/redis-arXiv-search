import React, { FC, useState } from 'react';

import { Header } from './views/Header';
import { Home } from './views/Home';
import { Footer } from './views/Footer';


export const Layout: FC = () => {
    const [papers, setPapers] = useState<any[]>([]);
    const [categories, setCategories] = useState<string[]>([]);
    const [years, setYears] = useState<string[]>([]);
    const [state, setState] = useState<string>('');

    return (
        <>
        <Header/>
        <Home setPapers={setPapers} papers={papers} categories={categories} setCategories={setCategories} years={years} setYears={setYears} searchState={state} setSearchState={setState}/>
        <Footer/>
        </>
    );
};

export default Layout;