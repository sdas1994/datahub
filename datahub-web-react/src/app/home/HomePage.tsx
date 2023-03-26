import React, { useEffect } from 'react';
import styled from 'styled-components/macro';
import { HomePageHeader } from './HomePageHeader';
import { HomePageBody } from './HomePageBody';
import analytics, { EventType } from '../analytics';
import { OnboardingTour } from '../onboarding/OnboardingTour';
import {
    GLOBAL_WELCOME_TO_DATAHUB_ID,
    HOME_PAGE_INGESTION_ID,
    HOME_PAGE_DOMAINS_ID,
    HOME_PAGE_MOST_POPULAR_ID,
    HOME_PAGE_PLATFORMS_ID,
    HOME_PAGE_SEARCH_BAR_ID,
} from '../onboarding/config/HomePageOnboardingConfig';

const Background = styled.div`
    width: 100%;
    height: 100vh;
    background: linear-gradient(
        135deg,
        ${(props) => props.theme.styles['homepage-background-lower-fade']} 0%,
        ${(props) => props.theme.styles['homepage-background-upper-fade']} 100%
    );
`;

export const HomePage = () => {
    useEffect(() => {
        analytics.event({ type: EventType.HomePageViewEvent });
    }, []);
    return (
        <Background>
            <OnboardingTour
                stepIds={[
                    GLOBAL_WELCOME_TO_DATAHUB_ID,
                    HOME_PAGE_INGESTION_ID,
                    HOME_PAGE_DOMAINS_ID,
                    HOME_PAGE_PLATFORMS_ID,
                    HOME_PAGE_MOST_POPULAR_ID,
                    HOME_PAGE_SEARCH_BAR_ID,
                ]}
            />
            <HomePageHeader />
            <HomePageBody />
        </Background>
    );
};
