import { FC } from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Layout from './Layout';
import { Admin } from './admin';

export const AppRoutes: FC = () => {

  return (
        <Router>
          <Routes>
            <Route path="/admin/*" element={<Admin />} />
          </Routes>
          <Routes>
            <Route path="/" element={<Layout/>}/>
          </Routes>
        </Router>
  );
};
