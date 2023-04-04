import React from 'react';
import { Image, Typography, Button } from 'antd';
import styled from 'styled-components';
import { ANTD_GRAY } from '../entity/shared/constants';
import { formatNumber } from './formatNumber';

const Container = styled(Button)`
    type: text;
    margin-right: 12px;
    margin-left: 12px;
    margin-bottom: 12px;
    padding-left: 24px;
    padding-right: 24px;
    width: 240px;
    height: 60px;
    display: flex;
    justify-content: left;
    border-radius: 16px;
    align-items: center;
    flex-direction: row;
    gap: 10px;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.01) 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition-duration: 0.4s;
    transtion-timing-function: linear;
    &&:hover {
        border-radius: 2px;
        border: 1px solid rgba(30, 226, 168, 0.2);
        background: linear-gradient(135deg, rgba(30, 226, 168, 0.2) 0%, rgba(255, 255, 255, 0.001) 100%);
        box-shadow: ${(props) => props.theme.styles['box-shadow-hover']};
    }
    white-space: unset;
`;

const PlatformLogo = styled(Image)`
    max-height: 28px;
    width: auto;
    object-fit: contain;
    background-color: transparent;
`;

const CountText = styled(Typography.Text)`
    margin-left: auto;
    font-size: 16px;
    color: ${ANTD_GRAY[8]};
`;

const LogoContainer = styled.div``;

const TitleContainer = styled.div``;

const Title = styled(Typography.Title)`
    &.ant-typography {
        color: ${ANTD_GRAY[7]};
    }
    word-break: break-word;
    padding-top: 7px;
`;

type Props = {
    logoUrl?: string;
    logoComponent?: React.ReactNode;
    name: string;
    count?: number;
    onClick?: () => void;
};

export const LogoCountCard = ({ logoUrl, logoComponent, name, count, onClick }: Props) => {
    return (
        <Container type="link" onClick={onClick}>
            <LogoContainer>
                {(logoUrl && <PlatformLogo preview={false} src={logoUrl} alt={name} />) || logoComponent}
            </LogoContainer>
            <TitleContainer>
                <Title
                    ellipsis={{
                        rows: 4,
                    }}
                    level={5}
                >
                    {name}
                </Title>
            </TitleContainer>
            {count !== undefined && <CountText>{formatNumber(count)}</CountText>}
        </Container>
    );
};
