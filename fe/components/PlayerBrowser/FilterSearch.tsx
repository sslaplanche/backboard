'use client'
import { useState, useEffect } from 'react'

const FilterSearch = ({ rows = [], filterColumns = []}) => {
    const [searchTerm, setSearchTerm] = useState('');

    const filteredRows = rows.filter((row) => {
        if (searchTerm.length > 0) {
            return filterColumns.some((column) => {
                return row[column].toLowerCase().includes(searchTerm.toLowerCase());
            });
        } else {
            return null;
        }
    });

    return (
        <div>
            <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search..."
                className='text-white py-2 px-4 rounded-md bg-white bg-opacity-10 border border-white w-full'
            />

            {/* Results */}
            <div className='max-h-[580px] overflow-scroll no-scrollbar'>
                <p>{filteredRows.length} results</p>
                {filteredRows.map((player, index) => (
                    <div key={index}>
                        
                        <div className='p-2  mt-2 flex justify-between border-1 border-b'>
                            <p>{player.first_name} {player.last_name}</p>
                        </div>

                    </div>
                ))}
            </div>
            
        </div>
    );
};


export default FilterSearch;
