import styled from 'styled-components';

export const Background = styled.div`
    width: 100%;
    height: 100%;
    min-height: 100vh;
    background: linear-gradient(
        135deg,
        ${(props) => props.theme.styles['homepage-background-lower-fade']} 0%,
        ${(props) => props.theme.styles['homepage-background-upper-fade']} 100%
    );
`;
